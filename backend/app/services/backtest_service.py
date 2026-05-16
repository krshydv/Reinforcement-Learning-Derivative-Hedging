import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Backtest
from app.quant.backtest import run_backtest_engine
from app.schemas.backtest import BacktestRequest, BacktestResult

class BacktestService:
    async def run_backtest(self, user_id: str, payload: BacktestRequest) -> BacktestResult:
        metrics = run_backtest_engine(payload.strategy, payload.steps)
        backtest_id = str(uuid.uuid4())
        async with AsyncSessionLocal() as session:
            session.add(Backtest(id=backtest_id, user_id=user_id, name=payload.name, status="completed", metrics=metrics))
            await session.commit()
        return BacktestResult(backtest_id=backtest_id, status="completed", metrics=metrics)
