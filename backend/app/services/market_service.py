from app.schemas.market import MarketConfig, MarketState
from app.quant.market_models import simulate_market

class MarketService:
    async def simulate(self, payload: MarketConfig) -> list[MarketState]:
        series = simulate_market(payload)
        return series
