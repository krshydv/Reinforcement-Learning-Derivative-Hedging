import uuid
from app.schemas.training import TrainingRequest, TrainingRun
from app.worker import celery_app

class TrainingService:
    async def start_training(self, user_id: str, payload: TrainingRequest) -> TrainingRun:
        run_id = str(uuid.uuid4())
        celery_app.send_task("app.worker.run_training", args=[payload.algorithm, payload.timesteps, run_id])
        return TrainingRun(run_id=run_id, status="started")

    async def stop_training(self, user_id: str, run_id: str) -> None:
        return None
