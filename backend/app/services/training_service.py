import uuid
from datetime import datetime
from sqlalchemy import select
from app.schemas.training import TrainingRequest, TrainingRun
from app.worker import celery_app
from app.db.session import AsyncSessionLocal
from app.db.models import TrainingRun as TrainingRunModel

class TrainingService:
    async def start_training(self, user_id: str, payload: TrainingRequest) -> TrainingRun:
        run_id = str(uuid.uuid4())
        async with AsyncSessionLocal() as session:
            session.add(TrainingRunModel(id=run_id, user_id=user_id, experiment_name=payload.experiment_name, algorithm=payload.algorithm, timesteps=payload.timesteps, status="running", created_at=datetime.utcnow(), updated_at=datetime.utcnow()))
            await session.commit()
        celery_app.send_task("app.worker.run_training", args=[payload.algorithm, payload.timesteps, run_id])
        return TrainingRun(run_id=run_id, status="running")

    async def stop_training(self, user_id: str, run_id: str) -> None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(TrainingRunModel).where(TrainingRunModel.id == run_id, TrainingRunModel.user_id == user_id))
            run = result.scalar_one_or_none()
            if run:
                run.status = "stopped"
                run.updated_at = datetime.utcnow()
                await session.commit()
