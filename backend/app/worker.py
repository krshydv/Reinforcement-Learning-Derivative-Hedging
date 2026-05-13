from celery import Celery
from app.core.config import settings
from app.quant.train import train_agent

celery_app = Celery("worker", broker=settings.celery_broker_url, backend=settings.celery_result_backend)

@celery_app.task(name="app.worker.run_training")
def run_training(algorithm: str, timesteps: int, run_id: str) -> str:
    train_agent(algorithm, timesteps, run_id)
    return run_id
