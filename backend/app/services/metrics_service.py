from app.quant.risk import risk_metrics
from app.quant.market_models import simulate_market
from app.schemas.market import MarketConfig
from app.quant.greeks import PortfolioGreeks

class MetricsService:
    async def latest_metrics(self, user_id: str) -> dict:
        config = MarketConfig(model="heston", steps=120, dt=0.01, spot=100, rate=0.02, vol=0.2)
        series = simulate_market(config)
        prices = [s.price for s in series]
        returns = [0.0] + [float((prices[i] - prices[i - 1]) / prices[i - 1]) for i in range(1, len(prices))]
        metrics = risk_metrics(returns)
        greeks = PortfolioGreeks().aggregate([
            {"spot": prices[-1], "strike": 100, "rate": 0.02, "vol": 0.2, "tau": 0.5, "call": True, "quantity": 10}
        ])
        return {**metrics, **greeks, "hedge_cost": metrics["cvar"] * 0.25}
