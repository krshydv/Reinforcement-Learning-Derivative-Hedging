from fastapi import APIRouter, Depends
from app.services.strategy_service import StrategyService
from app.services.auth_service import require_permission

router = APIRouter()

@router.get("/benchmarks")
async def benchmarks(user=Depends(require_permission("access"))) -> dict:
    return await StrategyService().benchmark(user.id)
