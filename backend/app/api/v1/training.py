from fastapi import APIRouter, Depends
from app.schemas.training import TrainingRequest, TrainingRun
from app.services.training_service import TrainingService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/start", response_model=TrainingRun)
async def start_training(payload: TrainingRequest, user=Depends(get_current_user)) -> TrainingRun:
    return await TrainingService().start_training(user.id, payload)

@router.post("/stop/{run_id}")
async def stop_training(run_id: str, user=Depends(get_current_user)) -> dict:
    await TrainingService().stop_training(user.id, run_id)
    return {"status": "stopped"}
