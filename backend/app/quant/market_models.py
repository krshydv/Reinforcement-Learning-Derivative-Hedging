import numpy as np
from app.schemas.market import MarketConfig, MarketState


def simulate_market(config: MarketConfig) -> list[MarketState]:
    assets = config.assets or ["asset"]
    n_assets = len(assets)
    corr = np.array(config.correlation) if config.correlation else np.eye(n_assets)
    dt = config.dt
    steps = config.steps
    prices = np.zeros((steps, n_assets))
    vols = np.zeros((steps, n_assets))
    prices[0] = config.spot
    vols[0] = config.vol
    regime = 0
    transition = np.array([[0.95, 0.05], [0.1, 0.9]])
    for t in range(1, steps):
        if config.regime_switching:
            regime = 0 if np.random.rand() < transition[regime, 0] else 1
        drift = config.rate + (0.01 if regime == 1 else 0.0)
        base_vol = config.vol * (1.4 if regime == 1 else 1.0)
        if config.model == "heston":
            kappa = 2.0
            theta = base_vol ** 2
            xi = 0.6
            z1 = correlated_normals(n_assets, corr)
            z2 = correlated_normals(n_assets, corr)
            vols[t] = np.abs(vols[t - 1] + kappa * (theta - vols[t - 1]) * dt + xi * np.sqrt(np.maximum(vols[t - 1], 0.0) * dt) * z2)
            diffusion = np.sqrt(np.maximum(vols[t], 0.0))
        else:
            z1 = correlated_normals(n_assets, corr)
            diffusion = np.full(n_assets, base_vol)
            vols[t] = diffusion ** 2 if config.model == "heston" else np.full(n_assets, base_vol)
        jump = np.zeros(n_assets)
        if config.model == "jump":
            lam = config.jump_intensity or 0.2
            mu_j = config.jump_mean or -0.1
            sigma_j = config.jump_vol or 0.3
            jump = np.random.poisson(lam * dt, size=n_assets) * np.random.normal(mu_j, sigma_j, size=n_assets)
        prices[t] = prices[t - 1] * np.exp((drift - 0.5 * diffusion ** 2) * dt + diffusion * np.sqrt(dt) * z1 + jump)
        if config.crash_prob and np.random.rand() < config.crash_prob:
            prices[t] *= 0.75
    series = []
    for t in range(steps):
        mid = float(prices[t, 0])
        spread = config.bid_ask_spread or 0.01
        slip = config.slippage or 0.0
        bid = mid * (1 - spread / 2 - slip)
        ask = mid * (1 + spread / 2 + slip)
        series.append(MarketState(
            t=t,
            price=mid,
            volatility=float(np.sqrt(np.maximum(vols[t, 0], 1e-8))),
            bid=bid,
            ask=ask,
            liquidity=config.liquidity or 1.0,
            regime=regime,
            prices=prices[t].tolist(),
            volatilities=(np.sqrt(np.maximum(vols[t], 1e-8))).tolist()
        ))
    return series


def correlated_normals(n_assets: int, corr: np.ndarray) -> np.ndarray:
    chol = np.linalg.cholesky(corr)
    return chol @ np.random.normal(size=n_assets)
