from pydantic import BaseModel

class PortfolioCreate(BaseModel):
    name: str

class PortfolioRead(BaseModel):
    id: str
    name: str

class PortfolioSnapshot(BaseModel):
    value: float
    pnl: float

class PortfolioOverview(BaseModel):
    netExposure: float
    grossExposure: float
    hedgeRatio: float
    positions: list[dict]
