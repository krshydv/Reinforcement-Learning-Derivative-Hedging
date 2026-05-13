from pydantic import BaseModel

class MarketConfig(BaseModel):
    model: str
    steps: int
    dt: float
    spot: float
    rate: float
    vol: float
    assets: list[str] | None = None
    correlation: list[list[float]] | None = None
    jump_intensity: float | None = None
    jump_mean: float | None = None
    jump_vol: float | None = None
    regime_switching: bool | None = None
    crash_prob: float | None = None
    bid_ask_spread: float | None = None
    slippage: float | None = None
    liquidity: float | None = None

class MarketState(BaseModel):
    t: int
    price: float
    volatility: float
    bid: float | None = None
    ask: float | None = None
    liquidity: float | None = None
    regime: int | None = None
    prices: list[float] | None = None
    volatilities: list[float] | None = None
