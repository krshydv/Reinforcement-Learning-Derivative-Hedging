import numpy as np
import gymnasium as gym
from gymnasium import spaces

class HedgingEnv(gym.Env):
    def __init__(self, steps: int = 252):
        self.steps = steps
        self.current_step = 0
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.state = np.zeros(12, dtype=np.float32)

    def reset(self, seed=None, options=None):
        self.current_step = 0
        self.state = np.random.normal(size=12).astype(np.float32)
        return self.state, {}

    def step(self, action):
        self.current_step += 1
        reward = -np.square(action).sum() + np.random.normal(0.01, 0.02)
        self.state = np.random.normal(size=12).astype(np.float32)
        terminated = self.current_step >= self.steps
        return self.state, float(reward), terminated, False, {}
