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
