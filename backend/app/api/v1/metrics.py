from fastapi import APIRouter, Depends, Request
from app.services.metrics_service import MetricsService
from app.services.auth_service import require_permission
from app.schemas.telemetry import TelemetryEventIn

router = APIRouter()

@router.get("/latest")
async def latest_metrics(request: Request, user=Depends(require_permission("access"))) -> dict:
    metrics = await MetricsService().latest_metrics(user.id)
    await request.app.state.telemetry.emit(TelemetryEventIn(
        channel="risk",
        event_type="metrics",
        payload=metrics,
        source="api",
    ), user_id=user.id)
    return metrics
