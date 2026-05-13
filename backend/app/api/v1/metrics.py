from fastapi import APIRouter, Depends
from app.services.metrics_service import MetricsService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/latest")
async def latest_metrics(user=Depends(get_current_user)) -> dict:
    return await MetricsService().latest_metrics(user.id)
