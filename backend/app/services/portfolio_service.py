import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Portfolio, PortfolioSnapshot
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioSnapshot as SnapshotSchema, PortfolioOverview

class PortfolioService:
    async def create_portfolio(self, user_id: str, payload: PortfolioCreate) -> PortfolioRead:
        async with AsyncSessionLocal() as session:
            portfolio = Portfolio(id=str(uuid.uuid4()), user_id=user_id, name=payload.name)
            session.add(portfolio)
            await session.commit()
            return PortfolioRead(id=portfolio.id, name=portfolio.name)

    async def get_portfolio(self, user_id: str, portfolio_id: str) -> PortfolioRead:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id))
            portfolio = result.scalar_one()
            return PortfolioRead(id=portfolio.id, name=portfolio.name)

    async def list_snapshots(self, user_id: str, portfolio_id: str) -> list[SnapshotSchema]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(PortfolioSnapshot).where(PortfolioSnapshot.portfolio_id == portfolio_id))
            snapshots = result.scalars().all()
            return [SnapshotSchema(value=s.value, pnl=s.pnl) for s in snapshots]

    async def overview(self, user_id: str) -> PortfolioOverview:
        positions = [
            {"symbol": "SPX", "quantity": 10, "avgPrice": 100.5, "delta": 5.1, "gamma": 0.12},
            {"symbol": "NDX", "quantity": -6, "avgPrice": 250.2, "delta": -2.8, "gamma": 0.08}
        ]
        net_exposure = sum(p["quantity"] * p["avgPrice"] for p in positions)
        gross_exposure = sum(abs(p["quantity"] * p["avgPrice"]) for p in positions)
        hedge_ratio = abs(sum(p["delta"] for p in positions)) / (gross_exposure + 1e-6)
        return PortfolioOverview(netExposure=net_exposure, grossExposure=gross_exposure, hedgeRatio=hedge_ratio, positions=positions)
