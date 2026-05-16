from fastapi import APIRouter, Depends
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioSnapshot, PortfolioOverview
from app.services.portfolio_service import PortfolioService
from app.services.auth_service import require_permission

router = APIRouter()

@router.post("/", response_model=PortfolioRead)
async def create_portfolio(payload: PortfolioCreate, user=Depends(require_permission("access"))) -> PortfolioRead:
    return await PortfolioService().create_portfolio(user.id, payload)

@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def get_portfolio(portfolio_id: str, user=Depends(require_permission("access"))) -> PortfolioRead:
    return await PortfolioService().get_portfolio(user.id, portfolio_id)

@router.get("/{portfolio_id}/snapshots", response_model=list[PortfolioSnapshot])
async def list_snapshots(portfolio_id: str, user=Depends(require_permission("access"))) -> list[PortfolioSnapshot]:
    return await PortfolioService().list_snapshots(user.id, portfolio_id)

@router.get("/overview", response_model=PortfolioOverview)
async def overview(user=Depends(require_permission("access"))) -> PortfolioOverview:
    return await PortfolioService().overview(user.id)
