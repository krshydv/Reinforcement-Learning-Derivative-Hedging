from pydantic import BaseModel

class MarketConfig(BaseModel):
    model: str
    steps: int
    dt: float
    spot: float
    rate: float
    vol: float

class MarketState(BaseModel):
    t: int
    price: float
    volatility: float
