from __future__ import annotations

from time import perf_counter
import numpy as np
from app.quant.backtest import BacktestEngine
from app.quant.options import OptionPricer
from app.quant.risk import risk_metrics
from app.quant.market_models import simulate_market
from app.schemas.market import MarketConfig


def _relative_error(base: float, value: float) -> float:
    if base == 0:
        return 0.0
    return float(abs(value - base) / abs(base))


def _market_returns(steps: int, seed: int) -> list[float]:
    series = simulate_market(MarketConfig(model="heston", steps=steps, dt=1 / 252, spot=100, rate=0.02, vol=0.2, seed=seed))
    prices = np.array([state.price for state in series], dtype=float)
    if len(prices) < 2:
        return []
    return ((prices[1:] - prices[:-1]) / prices[:-1]).tolist()


def run_benchmarks(config: dict) -> dict:
    seed = int(config.get("seed", 7))
    np.random.seed(seed)
    spot = float(config.get("spot", 100.0))
    strike = float(config.get("strike", 100.0))
    rate = float(config.get("rate", 0.02))
    vol = float(config.get("vol", 0.2))
    tau = float(config.get("tau", 1.0))
    paths = int(config.get("paths", 50_000))
    steps = int(config.get("steps", 252))
    include_backtests = bool(config.get("include_backtests", True))
    include_risk = bool(config.get("include_risk", True))

    timings: dict[str, float] = {}
    pricer = OptionPricer()

    start = perf_counter()
    bs_price = pricer.black_scholes(spot=spot, strike=strike, rate=rate, vol=vol, tau=tau, call=True)
    mc_price = pricer.monte_carlo(spot=spot, strike=strike, rate=rate, vol=vol, tau=tau, call=True, paths=paths)
    heston_price = pricer.heston_monte_carlo(
        spot=spot,
        strike=strike,
        rate=rate,
        v0=vol ** 2,
        kappa=1.6,
        theta=vol ** 2,
        xi=0.5,
        rho=-0.4,
        tau=tau,
        call=True,
        paths=max(10_000, paths // 3),
        steps=200,
    )
    merton_price = pricer.merton_jump_monte_carlo(
        spot=spot,
        strike=strike,
        rate=rate,
        vol=vol,
        tau=tau,
        call=True,
        jump_intensity=0.3,
        jump_mean=-0.08,
        jump_vol=0.25,
        paths=max(10_000, paths // 2),
    )
    implied_vol = pricer.implied_vol(price=bs_price, spot=spot, strike=strike, rate=rate, tau=tau, call=True)
    timings["pricing_ms"] = (perf_counter() - start) * 1000

    pricing = {
        "black_scholes": bs_price,
        "monte_carlo": mc_price,
        "heston_monte_carlo": heston_price,
        "merton_jump_monte_carlo": merton_price,
        "implied_vol": implied_vol,
        "relative_error_mc": _relative_error(bs_price, mc_price),
        "relative_error_heston": _relative_error(bs_price, heston_price),
        "relative_error_merton": _relative_error(bs_price, merton_price),
    }

    risk = None
    if include_risk:
        start = perf_counter()
        returns = _market_returns(steps=steps, seed=seed)
        risk = risk_metrics(returns)
        timings["risk_ms"] = (perf_counter() - start) * 1000

    backtests = None
    if include_backtests:
        start = perf_counter()
        engine = BacktestEngine(steps=steps)
        backtests = {}
        for strat in ["delta", "delta_gamma", "static"]:
            result = engine.run(strat)
            backtests[strat] = {"pnl": result.pnl, **result.metrics}
        timings["backtests_ms"] = (perf_counter() - start) * 1000

    return {"pricing": pricing, "risk": risk, "backtests": backtests, "timings": timings}
