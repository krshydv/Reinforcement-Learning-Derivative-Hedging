import numpy as np

def run_backtest_engine(strategy: str, steps: int) -> dict:
    pnl = np.random.normal(0.1, 0.2, steps).cumsum()
    drawdown = np.min(pnl - np.maximum.accumulate(pnl))
    return {"pnl": float(pnl[-1]), "max_drawdown": float(drawdown), "sharpe": float(np.mean(pnl) / (np.std(pnl) + 1e-6))}
