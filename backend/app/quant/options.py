import numpy as np
from scipy.stats import norm

class OptionPricer:
    def black_scholes(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool) -> float:
        d1 = (np.log(spot / strike) + (rate + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d2 = d1 - vol * np.sqrt(tau)
        if call:
            return spot * norm.cdf(d1) - strike * np.exp(-rate * tau) * norm.cdf(d2)
        return strike * np.exp(-rate * tau) * norm.cdf(-d2) - spot * norm.cdf(-d1)

    def greeks(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool) -> dict:
        d1 = (np.log(spot / strike) + (rate + 0.5 * vol ** 2) * tau) / (vol * np.sqrt(tau))
        d2 = d1 - vol * np.sqrt(tau)
        delta = norm.cdf(d1) if call else -norm.cdf(-d1)
        gamma = norm.pdf(d1) / (spot * vol * np.sqrt(tau))
        vega = spot * norm.pdf(d1) * np.sqrt(tau)
        theta = -(spot * norm.pdf(d1) * vol) / (2 * np.sqrt(tau)) - rate * strike * np.exp(-rate * tau) * norm.cdf(d2 if call else -d2)
        rho = strike * tau * np.exp(-rate * tau) * norm.cdf(d2 if call else -d2)
        return {"delta": delta, "gamma": gamma, "vega": vega, "theta": theta, "rho": rho}

    def monte_carlo(self, spot: float, strike: float, rate: float, vol: float, tau: float, call: bool, paths: int = 50000) -> float:
        z = np.random.normal(size=paths)
        st = spot * np.exp((rate - 0.5 * vol ** 2) * tau + vol * np.sqrt(tau) * z)
        payoff = np.maximum(st - strike, 0) if call else np.maximum(strike - st, 0)
        return np.exp(-rate * tau) * payoff.mean()
