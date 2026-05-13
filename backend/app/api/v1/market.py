from fastapi import APIRouter, Depends
from app.schemas.market import MarketConfig, MarketState
from app.services.market_service import MarketService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/simulate", response_model=list[MarketState])
async def simulate_market(payload: MarketConfig, user=Depends(get_current_user)) -> list[MarketState]:
    return await MarketService().simulate(payload)
