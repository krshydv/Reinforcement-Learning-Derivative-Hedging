from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.training import TrainingRequest, TrainingRun
from app.schemas.telemetry import TelemetryEventIn
from app.services.training_service import TrainingService
from app.services.auth_service import require_permission

router = APIRouter()

@router.post("/start", response_model=TrainingRun)
async def start_training(payload: TrainingRequest, request: Request, user=Depends(require_permission("access"))) -> TrainingRun:
    run = await TrainingService().start_training(user.id, payload)
    gateway = request.app.state.telemetry
    await gateway.emit(TelemetryEventIn(
        channel="training",
        event_type="run_started",
        payload={"run_id": run.run_id, "experiment": run.experiment_name, "algorithm": run.algorithm},
        source="api",
        run_id=run.run_id,
    ), user_id=user.id)
    await request.app.state.websocket_manager.broadcast({
        "type": "training_status",
        "run_id": run.run_id,
        "status": run.status,
        "experiment": run.experiment_name
    })
    return run


@router.get("/", response_model=list[TrainingRun])
async def list_training_runs(user=Depends(require_permission("access"))) -> list[TrainingRun]:
    return await TrainingService().list_runs(user.id)


@router.get("/{run_id}", response_model=TrainingRun)
async def get_training_run(run_id: str, user=Depends(require_permission("access"))) -> TrainingRun:
    run = await TrainingService().get_run(user.id, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="training run not found")
    return run

@router.post("/stop/{run_id}")
async def stop_training(run_id: str, request: Request, user=Depends(require_permission("access"))) -> dict:
    await TrainingService().stop_training(user.id, run_id)
    gateway = request.app.state.telemetry
    await gateway.emit(TelemetryEventIn(
        channel="training",
        event_type="run_stopped",
        payload={"run_id": run_id},
        source="api",
        run_id=run_id,
    ), user_id=user.id)
    await request.app.state.websocket_manager.broadcast({
        "type": "training_status",
        "run_id": run_id,
        "status": "stopped"
    })
    return {"status": "stopped"}
