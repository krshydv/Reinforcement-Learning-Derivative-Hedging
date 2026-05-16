from celery import Celery
from datetime import datetime
import asyncio
from sqlalchemy import select
from app.core.config import settings
from app.quant.train import train_agent
from app.db.session import AsyncSessionLocal
from app.db.models import TrainingRun

celery_app = Celery("worker", broker=settings.celery_broker_url, backend=settings.celery_result_backend)
celery_app.conf.worker_shutdown_timeout = 30

async def _mark_run(run_id: str, status: str) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TrainingRun).where(TrainingRun.id == run_id))
        run = result.scalar_one_or_none()
        if run:
            run.status = status
            run.updated_at = datetime.utcnow()
            await session.commit()

@celery_app.task(name="app.worker.run_training")
def run_training(algorithm: str, timesteps: int, run_id: str) -> str:
    asyncio.run(_mark_run(run_id, "running"))
    train_agent(algorithm, timesteps, run_id)
    asyncio.run(_mark_run(run_id, "completed"))
    return run_id
