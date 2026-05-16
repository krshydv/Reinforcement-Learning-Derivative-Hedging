import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Portfolio, PortfolioSnapshot, Position
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioSnapshot as SnapshotSchema, PortfolioOverview

class PortfolioService:
    async def create_portfolio(self, user_id: str, payload: PortfolioCreate) -> PortfolioRead:
        async with AsyncSessionLocal() as session:
            portfolio = Portfolio(id=str(uuid.uuid4()), user_id=user_id, name=payload.name)
            session.add(portfolio)
            session.add(PortfolioSnapshot(id=str(uuid.uuid4()), portfolio_id=portfolio.id, value=0.0, pnl=0.0))
            await session.commit()
            return PortfolioRead(id=portfolio.id, name=portfolio.name)

    async def get_portfolio(self, user_id: str, portfolio_id: str) -> PortfolioRead:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id))
            portfolio = result.scalar_one()
            return PortfolioRead(id=portfolio.id, name=portfolio.name)

    async def list_snapshots(self, user_id: str, portfolio_id: str) -> list[SnapshotSchema]:
        async with AsyncSessionLocal() as session:
            portfolio = await session.execute(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id))
            if not portfolio.scalar_one_or_none():
                return []
            result = await session.execute(select(PortfolioSnapshot).where(PortfolioSnapshot.portfolio_id == portfolio_id))
            snapshots = result.scalars().all()
            return [SnapshotSchema(value=s.value, pnl=s.pnl) for s in snapshots]

    async def overview(self, user_id: str) -> PortfolioOverview:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Position.symbol, Position.quantity, Position.avg_price)
                .join(Portfolio, Portfolio.id == Position.portfolio_id)
                .where(Portfolio.user_id == user_id)
            )
            positions = [{"symbol": symbol, "quantity": quantity, "avgPrice": avg_price} for symbol, quantity, avg_price in result.all()]
            net_exposure = sum(p["quantity"] * p["avgPrice"] for p in positions)
            gross_exposure = sum(abs(p["quantity"] * p["avgPrice"]) for p in positions)
            hedge_ratio = 0.0 if gross_exposure == 0 else abs(net_exposure) / gross_exposure
            return PortfolioOverview(netExposure=net_exposure, grossExposure=gross_exposure, hedgeRatio=hedge_ratio, positions=positions)
