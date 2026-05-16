from fastapi import APIRouter, Depends
from app.services.metrics_service import MetricsService
from app.services.auth_service import require_permission

router = APIRouter()

@router.get("/latest")
async def latest_metrics(user=Depends(require_permission("access"))) -> dict:
    return await MetricsService().latest_metrics(user.id)
