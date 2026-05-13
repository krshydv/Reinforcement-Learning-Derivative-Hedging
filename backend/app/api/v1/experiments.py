from fastapi import APIRouter, Depends
from app.schemas.experiment import ExperimentCreate, ExperimentRead
from app.services.experiment_service import ExperimentService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/", response_model=ExperimentRead)
async def create_experiment(payload: ExperimentCreate, user=Depends(get_current_user)) -> ExperimentRead:
    return await ExperimentService().create_experiment(user.id, payload)

@router.get("/", response_model=list[ExperimentRead])
async def list_experiments(user=Depends(get_current_user)) -> list[ExperimentRead]:
    return await ExperimentService().list_experiments(user.id)
