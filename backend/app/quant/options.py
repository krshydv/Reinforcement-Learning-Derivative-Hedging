import numpy as np
from scipy.stats import norm

class OptionPricer:
    def black_scholes(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool) -> float:
        if tau <= 0 or vol <= 0:
            intrinsic = max(0.0, spot - strike) if call else max(0.0, strike - spot)
            return intrinsic
        d1 = (np.log(spot / strike) + (rate + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d2 = d1 - vol * np.sqrt(tau)
        if call:
            return spot * norm.cdf(d1) - strike * np.exp(-rate * tau) * norm.cdf(d2)
        return strike * np.exp(-rate * tau) * norm.cdf(-d2) - spot * norm.cdf(-d1)

    def greeks(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool) -> dict:
        if tau <= 0 or vol <= 0:
            delta = 1.0 if spot > strike and call else -1.0 if spot < strike and not call else 0.0
            return {"delta": delta, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        d1 = (np.log(spot / strike) + (rate + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d2 = d1 - vol * np.sqrt(tau)
        delta = norm.cdf(d1) if call else -norm.cdf(-d1)
        gamma = norm.pdf(d1) / (spot * vol * np.sqrt(tau))
        vega = spot * norm.pdf(d1) * np.sqrt(tau)
        theta = -(spot * norm.pdf(d1) * vol) / (2 * np.sqrt(tau)) - rate * strike * np.exp(-rate * tau) * norm.cdf(d2 if call else -d2)
        rho = strike * tau * np.exp(-rate * tau) * norm.cdf(d2 if call else -d2)
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    def monte_carlo(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool, paths: int = 100000) -> float:
        z = np.random.normal(size=paths)
        st = spot * np.exp((rate - 0.5 * vol ** 2) * tau + vol * np.sqrt(tau) * z)
        payoff = np.maximum(st - strike, 0) if call else np.maximum(strike - st, 0)
        return float(np.exp(-rate * tau) * payoff.mean())

    def heston_monte_carlo(self, spot: float, strike: float, rate: float, v0: float, kappa: float, theta: float, xi: float, rho: float, tau: float, call: bool, paths: int = 60000, steps: int = 200) -> float:
        dt = tau / steps
        v = np.full(paths, v0)
        s = np.full(paths, spot)
        for _ in range(steps):
            z1 = np.random.normal(size=paths)
            z2 = rho * z1 + np.sqrt(1 - rho ** 2) * np.random.normal(size=paths)
            v = np.maximum(v + kappa * (theta - v) * dt + xi * np.sqrt(np.maximum(v, 0)) * np.sqrt(dt) * z2, 0.0)
            s = s * np.exp((rate - 0.5 * v) * dt + np.sqrt(v * dt) * z1)
        payoff = np.maximum(s - strike, 0) if call else np.maximum(strike - s, 0)
        return float(np.exp(-rate * tau) * payoff.mean())

    def merton_jump_monte_carlo(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool, jump_intensity: float, jump_mean: float, jump_vol: float, paths: int = 80000) -> float:
        n = np.random.poisson(jump_intensity * tau, size=paths)
        jump_sum = np.random.normal(jump_mean, jump_vol, size=paths) * n
        z = np.random.normal(size=paths)
        st = spot * np.exp((rate - 0.5 * vol ** 2 - jump_intensity * (np.exp(jump_mean + 0.5 * jump_vol ** 2) - 1)) * tau + vol * np.sqrt(tau) * z + jump_sum)
        payoff = np.maximum(st - strike, 0) if call else np.maximum(strike - st, 0)
        return float(np.exp(-rate * tau) * payoff.mean())

    def implied_vol(self, price: float, spot: float, strike: float, rate: float, tau: float, call: bool) -> float:
        vol = 0.2
        for _ in range(100):
            bs = self.black_scholes(spot, strike, rate, vol, tau, call)
            vega = self.greeks(spot, strike, rate, vol, tau, call)["vega"]
            if vega < 1e-8:
                break
            vol = max(1e-6, vol + (price - bs) / vega)
        return vol
