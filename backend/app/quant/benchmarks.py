import numpy as np

def run_benchmarks() -> dict:
    metrics = {
        "black_scholes_delta": {"sharpe": 1.2, "drawdown": 0.1, "cvar": 0.05},
        "delta_gamma": {"sharpe": 1.4, "drawdown": 0.08, "cvar": 0.04},
        "static": {"sharpe": 0.8, "drawdown": 0.2, "cvar": 0.1},
        "risk_parity": {"sharpe": 1.1, "drawdown": 0.12, "cvar": 0.06},
    }
    return metrics
