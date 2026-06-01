from pathlib import Path
import random
import numpy as np
import torch
from stable_baselines3 import PPO, SAC, TD3, DQN, A2C
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.callbacks import (
    BaseCallback,
    CheckpointCallback,
    EvalCallback,
    StopTrainingOnNoModelImprovement,
)
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv, VecNormalize
from stable_baselines3.common.monitor import Monitor
from app.quant.env import HedgingEnv
from app.quant.features import TransformerFeatureExtractor
from app.quant.rl_config import TrainConfig
from app.core.config import settings
from app.services.telemetry_service import SyncTelemetryPublisher
from app.schemas.telemetry import TelemetryEventIn

ALGOS = {"PPO": PPO, "SAC": SAC, "TD3": TD3, "DQN": DQN, "A2C": A2C, "LSTM": RecurrentPPO}


class TelemetryCallback(BaseCallback):
    def __init__(self, run_id: str, publisher: SyncTelemetryPublisher, log_interval: int, checkpoint_interval: int) -> None:
        super().__init__()
        self.run_id = run_id
        self.publisher = publisher
        self.log_interval = max(1, log_interval)
        self.checkpoint_interval = max(1, checkpoint_interval)
        self._last_emit = 0

    def _on_step(self) -> bool:
        if self.n_calls - self._last_emit >= self.log_interval:
            rewards = self.locals.get("rewards")
            actions = self.locals.get("actions")
            reward_mean = float(np.mean(rewards)) if rewards is not None else 0.0
            action_mean = float(np.mean(actions)) if actions is not None else 0.0
            action_std = float(np.std(actions)) if actions is not None else 0.0
            payload = {
                "step": int(self.num_timesteps),
                "reward_mean": reward_mean,
                "action_mean": action_mean,
                "action_std": action_std,
            }
            if not np.isfinite(reward_mean):
                payload["anomaly"] = "reward_nan"
            self.publisher.emit(
                TelemetryEventIn(
                    channel="training.metrics",
                    event_type="metrics",
                    payload=payload,
                    source="trainer",
                    run_id=self.run_id,
                )
            )
            self._last_emit = self.n_calls

        if self.n_calls % self.checkpoint_interval == 0:
            self.publisher.emit(
                TelemetryEventIn(
                    channel="training",
                    event_type="checkpoint",
                    payload={"step": int(self.num_timesteps)},
                    source="trainer",
                    run_id=self.run_id,
                )
            )
        return True


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def make_env(seed: int, reward_scale: float):
    def _init():
        env = HedgingEnv(seed=seed, reward_scale=reward_scale)
        return Monitor(env)

    return _init


def train_agent(config: TrainConfig, run_id: str) -> None:
    try:
        import mlflow
    except ModuleNotFoundError:
        mlflow = None
    try:
        import wandb
    except ModuleNotFoundError:
        wandb = None

    algo_key = config.algorithm.upper()
    algo = ALGOS.get(algo_key, PPO)
    seed_everything(config.seed)
    n_envs = max(1, config.n_envs)
    env_fns = [make_env(config.seed + i, config.reward_scale) for i in range(n_envs)]
    vec_env = SubprocVecEnv(env_fns) if n_envs > 1 else DummyVecEnv(env_fns)
    if config.normalize_obs or config.normalize_reward:
        vec_env = VecNormalize(
            vec_env,
            norm_obs=config.normalize_obs,
            norm_reward=config.normalize_reward,
            clip_obs=10.0,
        )

    eval_env = DummyVecEnv([make_env(config.seed + 999, config.reward_scale)])
    if config.normalize_obs or config.normalize_reward:
        eval_env = VecNormalize(
            eval_env,
            norm_obs=config.normalize_obs,
            norm_reward=False,
            clip_obs=10.0,
        )

    log_dir = Path(settings.training_log_dir)
    ckpt_dir = Path(settings.checkpoint_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    policy = "MlpLstmPolicy" if algo_key == "LSTM" else "MlpPolicy"
    policy_kwargs = {}
    if config.use_transformer:
        policy_kwargs = {
            "features_extractor_class": TransformerFeatureExtractor,
            "features_extractor_kwargs": {"features_dim": 64},
        }
    model = algo(
        policy,
        vec_env,
        verbose=0,
        tensorboard_log=str(log_dir),
        policy_kwargs=policy_kwargs,
        learning_rate=config.learning_rate,
        gamma=config.gamma,
        gae_lambda=config.gae_lambda,
        clip_range=config.clip_range if algo_key == "PPO" else None,
    )
    checkpoint_freq = max(1000, int(config.eval_freq))
    checkpoint = CheckpointCallback(save_freq=checkpoint_freq, save_path=str(ckpt_dir), name_prefix=f"{run_id}_{algo_key}")
    stop_cb = StopTrainingOnNoModelImprovement(max_no_improvement_evals=config.patience, min_evals=3, verbose=0)
    eval_cb = EvalCallback(
        eval_env,
        eval_freq=config.eval_freq,
        n_eval_episodes=config.eval_episodes,
        best_model_save_path=str(ckpt_dir),
        callback_after_eval=stop_cb,
        deterministic=True,
    )
    publisher = SyncTelemetryPublisher.create(settings.redis_url)
    telemetry_cb = TelemetryCallback(run_id, publisher, config.log_interval, checkpoint_freq)

    if mlflow is not None:
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment("rl-hedging")
    try:
        if mlflow is not None:
            with mlflow.start_run(run_name=run_id):
                mlflow.log_param("algorithm", algo_key)
                mlflow.log_param("timesteps", config.timesteps)
                mlflow.log_param("n_envs", n_envs)
                mlflow.log_param("seed", config.seed)
                model.learn(total_timesteps=config.timesteps, callback=[checkpoint, eval_cb, telemetry_cb])
                mlflow.log_artifact(str(ckpt_dir))
                if isinstance(vec_env, VecNormalize):
                    vec_env.save(str(ckpt_dir / f"{run_id}_{algo_key}_vecnormalize.pkl"))
        else:
            model.learn(total_timesteps=config.timesteps, callback=[checkpoint, eval_cb, telemetry_cb])
            if isinstance(vec_env, VecNormalize):
                vec_env.save(str(ckpt_dir / f"{run_id}_{algo_key}_vecnormalize.pkl"))
    finally:
        publisher.close()

    if wandb is not None and settings.wand_b_api_key:
        wandb.login(key=settings.wand_b_api_key)
        wandb.init(project=settings.wand_b_project, entity=settings.wand_b_entity, name=run_id)
        wandb.log({"timesteps": config.timesteps, "algorithm": algo_key})
        wandb.finish()

    vec_env.close()
    eval_env.close()
