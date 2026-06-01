from fastapi import APIRouter, Depends
from app.schemas.backtest import BacktestRequest, BacktestResult
from app.services.backtest_service import BacktestService
from app.services.auth_service import require_permission

router = APIRouter()

@router.post("/run", response_model=BacktestResult)
async def run_backtest(payload: BacktestRequest, user=Depends(require_permission("access"))) -> BacktestResult:
    return await BacktestService().run_backtest(user.id, payload)
