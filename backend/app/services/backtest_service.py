from app.quant.backtest import run_backtest_engine
from app.schemas.backtest import BacktestRequest, BacktestResult

class BacktestService:
    async def run_backtest(self, user_id: str, payload: BacktestRequest) -> BacktestResult:
        metrics = run_backtest_engine(payload.strategy, payload.steps)
        return BacktestResult(backtest_id=payload.name, status="completed", metrics=metrics)
