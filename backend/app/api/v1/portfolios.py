from __future__ import annotations

from fastapi import APIRouter, Depends, Request, HTTPException
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioSnapshot, PortfolioOverview
from app.services.portfolio_service import PortfolioService
from app.services.auth_service import require_permission
from app.schemas.telemetry import TelemetryEventIn

router = APIRouter()

@router.post("/", response_model=PortfolioRead)
async def create_portfolio(payload: PortfolioCreate, user=Depends(require_permission("access"))) -> PortfolioRead:
    return await PortfolioService().create_portfolio(user.id, payload)

@router.get("/{portfolio_id}/snapshots", response_model=list[PortfolioSnapshot])
async def list_snapshots(portfolio_id: str, user=Depends(require_permission("access"))) -> list[PortfolioSnapshot]:
    return await PortfolioService().list_snapshots(user.id, portfolio_id)

@router.get("/overview", response_model=PortfolioOverview)
async def overview(request: Request, user=Depends(require_permission("access"))) -> PortfolioOverview:
    overview_data = await PortfolioService().overview(user.id)
    await request.app.state.telemetry.emit(TelemetryEventIn(
        channel="portfolio",
        event_type="overview",
        payload=overview_data.model_dump(),
        source="api",
    ), user_id=user.id)
    return overview_data

@router.get("/{portfolio_id}", response_model=PortfolioRead)
async def get_portfolio(portfolio_id: str, user=Depends(require_permission("access"))) -> PortfolioRead:
    portfolio = await PortfolioService().get_portfolio(user.id, portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="portfolio not found")
    return portfolio
