import mlflow
import wandb
import numpy as np
from stable_baselines3 import PPO, SAC, TD3, DQN, A2C
from app.quant.env import HedgingEnv
from app.core.config import settings

ALGOS = {"PPO": PPO, "SAC": SAC, "TD3": TD3, "DQN": DQN, "A2C": A2C}

def train_agent(algorithm: str, timesteps: int, run_id: str) -> None:
    env = HedgingEnv()
    algo = ALGOS.get(algorithm.upper(), PPO)
    model = algo("MlpPolicy", env, verbose=0)
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment("rl-hedging")
    with mlflow.start_run(run_name=run_id):
        model.learn(total_timesteps=timesteps)
        mlflow.log_param("algorithm", algorithm)
        mlflow.log_metric("timesteps", timesteps)
    if settings.wand_b_api_key:
        wandb.login(key=settings.wand_b_api_key)
        wandb.init(project=settings.wand_b_project, entity=settings.wand_b_entity, name=run_id)
        wandb.log({"timesteps": timesteps})
        wandb.finish()
