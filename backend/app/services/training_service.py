from __future__ import annotations

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
            session.add(
                TrainingRunModel(
                    id=run_id,
                    user_id=user_id,
                    experiment_name=payload.experiment_name,
                    algorithm=payload.algorithm,
                    timesteps=payload.timesteps,
                    status="queued",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
            )
            await session.commit()
        celery_app.send_task("app.worker.run_training", args=[payload.model_dump(), run_id])
        return TrainingRun(
            run_id=run_id,
            experiment_name=payload.experiment_name,
            algorithm=payload.algorithm,
            timesteps=payload.timesteps,
            status="queued",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

    async def stop_training(self, user_id: str, run_id: str) -> None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(TrainingRunModel).where(TrainingRunModel.id == run_id, TrainingRunModel.user_id == user_id))
            run = result.scalar_one_or_none()
            if run:
                run.status = "stopped"
                run.updated_at = datetime.utcnow()
                await session.commit()

    async def list_runs(self, user_id: str) -> list[TrainingRun]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(TrainingRunModel).where(TrainingRunModel.user_id == user_id))
            runs = result.scalars().all()
            return [
                TrainingRun(
                    run_id=run.id,
                    experiment_name=run.experiment_name,
                    algorithm=run.algorithm,
                    timesteps=run.timesteps,
                    status=run.status,
                    created_at=run.created_at,
                    updated_at=run.updated_at,
                )
                for run in runs
            ]

    async def get_run(self, user_id: str, run_id: str) -> TrainingRun | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(TrainingRunModel).where(TrainingRunModel.id == run_id, TrainingRunModel.user_id == user_id))
            run = result.scalar_one_or_none()
            if not run:
                return None
            return TrainingRun(
                run_id=run.id,
                experiment_name=run.experiment_name,
                algorithm=run.algorithm,
                timesteps=run.timesteps,
                status=run.status,
                created_at=run.created_at,
                updated_at=run.updated_at,
            )
