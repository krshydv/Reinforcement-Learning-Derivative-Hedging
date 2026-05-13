import numpy as np
import gymnasium as gym
from gymnasium import spaces
from app.quant.market_models import simulate_market
from app.schemas.market import MarketConfig
from app.quant.risk import risk_metrics

class HedgingEnv(gym.Env):
    def __init__(self, steps: int = 252, cost: float = 0.001, cvar_alpha: float = 0.05):
        self.steps = steps
        self.cost = cost
        self.cvar_alpha = cvar_alpha
        self.current_step = 0
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(12,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)
        self.state = np.zeros(12, dtype=np.float32)
        self.pnl = 0.0
        self.drawdown = 0.0
        self.max_pnl = 0.0
        self.returns = []
        self.series = []

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.pnl = 0.0
        self.drawdown = 0.0
        self.max_pnl = 0.0
        self.returns = []
        self.series = simulate_market(MarketConfig(model="heston", steps=self.steps, dt=1 / 252, spot=100, rate=0.02, vol=0.2))
        self.state = self._build_state(0)
        return self.state, {}

    def step(self, action):
        self.current_step += 1
        hedge_error = float(np.dot(self.state[:3], action))
        transaction_cost = self.cost * float(np.sum(np.abs(action)))
        self.pnl += -hedge_error - transaction_cost
        self.max_pnl = max(self.max_pnl, self.pnl)
        self.drawdown = min(self.drawdown, self.pnl - self.max_pnl)
        self.returns.append(self.pnl)
        cvar_penalty = abs(self._cvar_penalty())
        reward = self.pnl - 0.5 * transaction_cost - 0.2 * abs(self.drawdown) - 0.3 * cvar_penalty
        self.state = self._build_state(self.current_step)
        terminated = self.current_step >= self.steps - 1
        return self.state, float(reward), terminated, False, {}

    def _build_state(self, idx: int) -> np.ndarray:
        point = self.series[idx]
        state = np.array([
            point.price,
            point.volatility,
            point.bid or point.price,
            point.ask or point.price,
            point.liquidity or 1.0,
            float(point.regime or 0),
            self.pnl,
            self.drawdown,
            self.max_pnl,
            self.returns[-1] if self.returns else 0.0,
            float(point.prices[0] if point.prices else point.price),
            float(point.volatilities[0] if point.volatilities else point.volatility)
        ], dtype=np.float32)
        return state

    def _cvar_penalty(self) -> float:
        if len(self.returns) < 5:
            return 0.0
        metrics = risk_metrics(self.returns)
        return metrics["cvar"]
