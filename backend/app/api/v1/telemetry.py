from fastapi import APIRouter, Depends, Request
from app.schemas.telemetry import TelemetryEventIn, TelemetryEvent, TelemetryReplay
from app.services.auth_service import require_permission

router = APIRouter()


@router.post("/emit", response_model=TelemetryEvent)
async def emit_telemetry(payload: TelemetryEventIn, request: Request, user=Depends(require_permission("access"))) -> TelemetryEvent:
    gateway = request.app.state.telemetry
    return await gateway.emit(payload, user_id=user.id)


@router.get("/replay", response_model=TelemetryReplay)
async def replay(request: Request, channel: str, limit: int = 100, user=Depends(require_permission("access"))) -> TelemetryReplay:
    _ = user
    gateway = request.app.state.telemetry
    events = await gateway.replay(channel, limit=limit)
    return TelemetryReplay(channel=channel, events=events)
