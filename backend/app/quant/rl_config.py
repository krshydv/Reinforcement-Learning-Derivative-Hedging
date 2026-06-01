from dataclasses import dataclass


@dataclass
class TrainConfig:
    algorithm: str = "PPO"
    timesteps: int = 200_000
    seed: int = 7
    n_envs: int = 4
    reward_scale: float = 1.0
    use_transformer: bool = False
    eval_freq: int = 5_000
    eval_episodes: int = 5
    patience: int = 3
    learning_rate: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_range: float = 0.2
    normalize_obs: bool = True
    normalize_reward: bool = True
    log_interval: int = 1000
