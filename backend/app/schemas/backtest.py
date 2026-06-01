from pydantic import BaseModel

class BacktestRequest(BaseModel):
    name: str
    strategy: str
    steps: int

class BacktestResult(BaseModel):
    backtest_id: str
    status: str
    metrics: dict
