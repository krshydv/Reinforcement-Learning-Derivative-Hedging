from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    id: str
    channel: str
    event_type: str
    timestamp: datetime
    payload: dict
    source: str = "api"
    run_id: str | None = None
    user_id: str | None = None


class TelemetryEventIn(BaseModel):
    channel: str
    event_type: str
    payload: dict = Field(default_factory=dict)
    source: str = "api"
    run_id: str | None = None


class TelemetryReplay(BaseModel):
    channel: str
    events: list[TelemetryEvent]
