from fastapi import APIRouter, Depends
from app.schemas.backtest import BacktestRequest, BacktestResult
from app.services.backtest_service import BacktestService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/run", response_model=BacktestResult)
async def run_backtest(payload: BacktestRequest, user=Depends(get_current_user)) -> BacktestResult:
    return await BacktestService().run_backtest(user.id, payload)
