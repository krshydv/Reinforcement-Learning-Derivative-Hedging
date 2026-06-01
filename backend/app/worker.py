from celery import Celery
from datetime import datetime
import asyncio
from sqlalchemy import select
from app.core.config import settings
from app.quant.rl_config import TrainConfig
from app.services.training_manager import TrainingManager
from app.services.telemetry_service import TelemetryGateway
from app.schemas.telemetry import TelemetryEventIn
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


async def _emit_training_event(run_id: str, event_type: str) -> None:
    gateway = TelemetryGateway.create(settings.redis_url)
    await gateway.emit(TelemetryEventIn(
        channel="training",
        event_type=event_type,
        payload={"run_id": run_id},
        source="worker",
        run_id=run_id,
    ))
    await gateway.close()


@celery_app.task(name="app.worker.run_training")
def run_training(payload: dict, run_id: str) -> str:
    asyncio.run(_mark_run(run_id, "running"))
    asyncio.run(_emit_training_event(run_id, "run_started"))
    try:
        config = TrainConfig(**payload)
        TrainingManager().run(config, run_id=run_id)
        asyncio.run(_mark_run(run_id, "completed"))
        asyncio.run(_emit_training_event(run_id, "run_completed"))
    except Exception:
        asyncio.run(_mark_run(run_id, "failed"))
        asyncio.run(_emit_training_event(run_id, "run_failed"))
        raise
    return run_id
