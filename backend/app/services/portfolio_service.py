import uuid
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.db.models import Portfolio, PortfolioSnapshot
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PortfolioSnapshot as SnapshotSchema

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
