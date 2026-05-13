from app.quant.backtest import BacktestEngine


def run_benchmarks() -> dict:
    engine = BacktestEngine(steps=252)
    results = {}
    for strat in ["delta", "delta_gamma", "static"]:
        res = engine.run("delta" if strat == "delta" else strat)
        results[strat] = res.metrics
    return results
