import numpy as np
from app.quant.options import OptionPricer

class PortfolioGreeks:
    def aggregate(self, positions: list[dict]) -> dict:
        pricer = OptionPricer()
        totals = {"delta": 0.0, "gamma": 0.0, "vega": 0.0, "theta": 0.0, "rho": 0.0}
        for p in positions:
            greeks = pricer.greeks(p["spot"], p["strike"], p["rate"], p["vol"], p["tau"], p["call"])
            for k in totals:
                totals[k] += greeks[k] * p["quantity"]
        return totals

class VolSurface:
    def generate(self, spot: float, rate: float, base_vol: float, strikes: list[float], tenors: list[float]) -> list[list[float]]:
        surface = []
        for tau in tenors:
            row = []
            for strike in strikes:
                moneyness = np.log(strike / spot)
                vol = base_vol * (1 + 0.25 * moneyness ** 2) * (1 + 0.1 * np.sqrt(tau))
                row.append(float(max(0.01, vol)))
            surface.append(row)
        return surface
