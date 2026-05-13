import numpy as np


def risk_metrics(returns: list[float], rf: float = 0.0) -> dict:
    if len(returns) == 0:
        return {"sharpe": 0.0, "sortino": 0.0, "max_drawdown": 0.0, "var": 0.0, "cvar": 0.0}
    r = np.array(returns, dtype=float)
    excess = r - rf
    sharpe = np.mean(excess) / (np.std(excess) + 1e-8) * np.sqrt(252)
    downside = excess[excess < 0]
    sortino = np.mean(excess) / (np.std(downside) + 1e-8) * np.sqrt(252)
    cumulative = np.cumprod(1 + r)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    max_drawdown = float(np.min(drawdown))
    sorted_returns = np.sort(r)
    var_index = int(0.05 * len(sorted_returns))
    var = float(sorted_returns[var_index])
    cvar = float(np.mean(sorted_returns[: var_index + 1]))
    return {"sharpe": float(sharpe), "sortino": float(sortino), "max_drawdown": max_drawdown, "var": var, "cvar": cvar}
