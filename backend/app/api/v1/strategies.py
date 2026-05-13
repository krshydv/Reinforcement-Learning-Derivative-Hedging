from fastapi import APIRouter, Depends
from app.services.strategy_service import StrategyService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/benchmarks")
async def benchmarks(user=Depends(get_current_user)) -> dict:
    return await StrategyService().benchmark(user.id)
