from dataclasses import dataclass
import numpy as np
from app.quant.options import OptionPricer
from app.quant.risk import risk_metrics
from app.quant.market_models import simulate_market
from app.schemas.market import MarketConfig

@dataclass
class Trade:
    step: int
    price: float
    quantity: float

@dataclass
class BacktestResult:
    pnl: float
    returns: list[float]
    trades: list[Trade]
    metrics: dict

class BacktestEngine:
    def __init__(self, steps: int = 252):
        self.steps = steps
        self.pricer = OptionPricer()

    def run(self, strategy: str) -> BacktestResult:
        series = simulate_market(MarketConfig(model="heston", steps=self.steps, dt=1 / 252, spot=100, rate=0.02, vol=0.2))
        prices = [s.price for s in series]
        trades = []
        cash = 0.0
        hedge_position = 0.0
        option_qty = 10.0
        returns = []
        for t in range(1, len(prices)):
            tau = max(1e-6, (self.steps - t) / 252)
            option_price = self.pricer.black_scholes(prices[t], 100, 0.02, 0.2, tau, True)
            greeks = self.pricer.greeks(prices[t], 100, 0.02, 0.2, tau, True)
            target_hedge = -greeks["delta"] * option_qty
            if strategy == "delta_gamma":
                target_hedge += -greeks["gamma"] * option_qty * 0.5
            if strategy == "static":
                target_hedge = 0.0
            trade_qty = target_hedge - hedge_position
            if trade_qty != 0:
                cash -= trade_qty * prices[t]
                hedge_position += trade_qty
                trades.append(Trade(step=t, price=prices[t], quantity=trade_qty))
            portfolio_value = cash + hedge_position * prices[t] + option_qty * option_price
            if t > 1:
                prev_value = cash + hedge_position * prices[t - 1] + option_qty * self.pricer.black_scholes(prices[t - 1], 100, 0.02, 0.2, tau + 1 / 252, True)
                returns.append((portfolio_value - prev_value) / prev_value)
        pnl = cash + hedge_position * prices[-1] + option_qty * self.pricer.black_scholes(prices[-1], 100, 0.02, 0.2, 1 / 252, True)
        metrics = risk_metrics(returns)
        return BacktestResult(pnl=float(pnl), returns=returns, trades=trades, metrics=metrics)

def run_backtest_engine(strategy: str, steps: int) -> dict:
    engine = BacktestEngine(steps=steps)
    result = engine.run(strategy)
    return {"pnl": result.pnl, **result.metrics}
