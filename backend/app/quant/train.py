from pathlib import Path
import mlflow
import wandb
from stable_baselines3 import PPO, SAC, TD3, DQN, A2C
from sb3_contrib import RecurrentPPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from app.quant.env import HedgingEnv
from app.quant.features import TransformerFeatureExtractor
from app.core.config import settings

ALGOS = {"PPO": PPO, "SAC": SAC, "TD3": TD3, "DQN": DQN, "A2C": A2C, "LSTM": RecurrentPPO}


def make_env():
    def _init():
        return Monitor(HedgingEnv())
    return _init


def train_agent(algorithm: str, timesteps: int, run_id: str, use_transformer: bool = False) -> None:
    algo_key = algorithm.upper()
    algo = ALGOS.get(algo_key, PPO)
    n_envs = max(1, settings.num_envs)
    vec_env = SubprocVecEnv([make_env() for _ in range(n_envs)]) if n_envs > 1 else DummyVecEnv([make_env()])
    log_dir = Path(settings.training_log_dir)
    ckpt_dir = Path(settings.checkpoint_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    policy = "MlpLstmPolicy" if algo_key == "LSTM" else "MlpPolicy"
    policy_kwargs = {}
    if use_transformer:
        policy_kwargs = {"features_extractor_class": TransformerFeatureExtractor, "features_extractor_kwargs": {"features_dim": 64}}
    model = algo(policy, vec_env, verbose=0, tensorboard_log=str(log_dir), policy_kwargs=policy_kwargs)
    checkpoint = CheckpointCallback(save_freq=5000, save_path=str(ckpt_dir), name_prefix=f"{run_id}_{algo_key}")
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("rl-hedging")
    with mlflow.start_run(run_name=run_id):
        mlflow.log_param("algorithm", algo_key)
        mlflow.log_param("timesteps", timesteps)
        mlflow.log_param("n_envs", n_envs)
        model.learn(total_timesteps=timesteps, callback=checkpoint)
        mlflow.log_artifact(str(ckpt_dir))
    if settings.wand_b_api_key:
        wandb.login(key=settings.wand_b_api_key)
        wandb.init(project=settings.wand_b_project, entity=settings.wand_b_entity, name=run_id)
        wandb.log({"timesteps": timesteps, "algorithm": algo_key})
        wandb.finish()
    vec_env.close()
