from fastapi import APIRouter, Depends
from app.schemas.market import MarketConfig, MarketState
from app.services.market_service import MarketService
from app.services.auth_service import require_permission

router = APIRouter()

@router.post("/simulate", response_model=list[MarketState])
async def simulate_market(payload: MarketConfig, user=Depends(require_permission("access"))) -> list[MarketState]:
    return await MarketService().simulate(payload)
