import uuid
import numpy as np
from app.schemas.market import MarketConfig, MarketState
from app.quant.market_models import simulate_gbm, simulate_heston, simulate_jump

class MarketService:
    async def simulate(self, payload: MarketConfig) -> list[MarketState]:
        if payload.model == "gbm":
            prices, vols = simulate_gbm(payload.spot, payload.rate, payload.vol, payload.steps, payload.dt)
        elif payload.model == "heston":
            prices, vols = simulate_heston(payload.spot, payload.rate, payload.vol, payload.steps, payload.dt)
        else:
            prices, vols = simulate_jump(payload.spot, payload.rate, payload.vol, payload.steps, payload.dt)
        return [MarketState(t=i, price=float(prices[i]), volatility=float(vols[i])) for i in range(payload.steps)]
