from app.db.session import AsyncSessionLocal
from app.db.models import Metric
from sqlalchemy import select

class MetricsService:
    async def latest_metrics(self, user_id: str) -> dict:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Metric).order_by(Metric.created_at.desc()).limit(50))
            metrics = result.scalars().all()
            return {m.name: m.value for m in metrics}
