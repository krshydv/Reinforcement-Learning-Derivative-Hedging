import numpy as np
import gymnasium as gym
from gymnasium import spaces

class HedgingEnv(gym.Env):
    def __init__(self, steps: int = 252, cost: float = 0.001):
        self.steps = steps
        self.cost = cost
        self.current_step = 0
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.state = np.zeros(12, dtype=np.float32)
        self.pnl = 0.0
        self.drawdown = 0.0
        self.max_pnl = 0.0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.pnl = 0.0
        self.drawdown = 0.0
        self.max_pnl = 0.0
        self.state = np.random.normal(size=12).astype(np.float32)
        return self.state, {}

    def step(self, action):
        self.current_step += 1
        hedge_error = float(np.dot(self.state[:3], action))
        transaction_cost = self.cost * float(np.sum(np.abs(action)))
        self.pnl += -hedge_error - transaction_cost + np.random.normal(0.01, 0.02)
        self.max_pnl = max(self.max_pnl, self.pnl)
        self.drawdown = min(self.drawdown, self.pnl - self.max_pnl)
        reward = self.pnl - 0.5 * transaction_cost - 0.2 * abs(self.drawdown)
        self.state = np.random.normal(size=12).astype(np.float32)
        terminated = self.current_step >= self.steps
        return self.state, float(reward), terminated, False, {}
