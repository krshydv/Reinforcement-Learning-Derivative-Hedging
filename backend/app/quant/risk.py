from __future__ import annotations

import numpy as np


def compute_drawdown(returns: np.ndarray) -> tuple[float, np.ndarray]:
    if returns.size == 0:
        return 0.0, np.array([])
    cumulative = np.cumprod(1 + returns)
    peak = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - peak) / peak
    return float(np.min(drawdown)), drawdown


def compute_var_cvar(returns: np.ndarray, alpha: float = 0.05) -> tuple[float, float]:
    if returns.size == 0:
        return 0.0, 0.0
    sorted_returns = np.sort(returns)
    var_index = max(int(alpha * len(sorted_returns)) - 1, 0)
    var = float(sorted_returns[var_index])
    cvar = float(np.mean(sorted_returns[: var_index + 1]))
    return var, cvar


def exposure_analytics(positions: list[dict]) -> dict:
    totals = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0, "notional": 0.0}
    for position in positions:
        qty = float(position.get("quantity", 0.0))
        spot = float(position.get("spot", 0.0))
        totals["notional"] += qty * spot
        for key in ["delta", "gamma", "vega", "theta", "rho"]:
            totals[key] += float(position.get(key, 0.0)) * qty
    return totals


def risk_decomposition(returns_matrix: np.ndarray, weights: np.ndarray, alpha: float = 0.05) -> dict:
    if returns_matrix.size == 0:
        return {"portfolio_var": 0.0, "marginal": [], "component": []}
    cov = np.cov(returns_matrix, rowvar=False)
    portfolio_var = float(weights.T @ cov @ weights)
    if portfolio_var <= 0:
        return {"portfolio_var": 0.0, "marginal": [0.0] * len(weights), "component": [0.0] * len(weights)}
    marginal = (cov @ weights) / np.sqrt(portfolio_var)
    component = weights * marginal
    return {
        "portfolio_var": float(np.sqrt(portfolio_var)),
        "marginal": [float(x) for x in marginal],
        "component": [float(x) for x in component],
    }


def stress_test(returns: list[float], shocks: list[dict]) -> list[dict]:
    base = np.array(returns, dtype=float)
    results = []
    for shock in shocks:
        shift = float(shock.get("shift", 0.0))
        scale = float(shock.get("scale", 1.0))
        shocked = base * scale + shift
        metrics = risk_metrics(shocked.tolist())
        results.append({"name": shock.get("name", "scenario"), **metrics})
    return results


def pnl_attribution(returns: np.ndarray, weights: np.ndarray) -> dict:
    if returns.size == 0:
        return {"total": 0.0, "by_asset": []}
    pnl_by_asset = returns.mean(axis=0) * weights
    total = float(np.sum(pnl_by_asset))
    return {"total": total, "by_asset": [float(x) for x in pnl_by_asset]}


def scenario_simulation(returns: list[float], scenarios: list[dict]) -> list[dict]:
    base = np.array(returns, dtype=float)
    outputs = []
    for scenario in scenarios:
        shift = float(scenario.get("shift", 0.0))
        scale = float(scenario.get("scale", 1.0))
        sim = base * scale + shift
        var, cvar = compute_var_cvar(sim)
        max_dd, _ = compute_drawdown(sim)
        outputs.append(
            {
                "name": scenario.get("name", "scenario"),
                "mean": float(np.mean(sim)) if sim.size else 0.0,
                "vol": float(np.std(sim)) if sim.size else 0.0,
                "var": var,
                "cvar": cvar,
                "max_drawdown": max_dd,
            }
        )
    return outputs


def risk_metrics(returns: list[float], rf: float = 0.0) -> dict:
    if len(returns) == 0:
        return {"sharpe": 0.0, "sortino": 0.0, "max_drawdown": 0.0, "var": 0.0, "cvar": 0.0}
    r = np.array(returns, dtype=float)
    excess = r - rf
    sharpe = np.mean(excess) / (np.std(excess) + 1e-8) * np.sqrt(252)
    downside = excess[excess < 0]
    sortino = np.mean(excess) / (np.std(downside) + 1e-8) * np.sqrt(252)
    max_drawdown, _ = compute_drawdown(r)
    var, cvar = compute_var_cvar(r)
    return {
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "max_drawdown": max_drawdown,
        "var": var,
        "cvar": cvar,
    }
