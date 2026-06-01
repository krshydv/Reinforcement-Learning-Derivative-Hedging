import time
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.schemas.telemetry import TelemetryEventIn


class TelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        gateway = getattr(request.app.state, "telemetry", None)
        if gateway:
            payload = TelemetryEventIn(
                channel="api.latency",
                event_type="http_request",
                payload={
                    "path": request.url.path,
                    "method": request.method,
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                },
                source="middleware",
            )
            asyncio.create_task(gateway.emit(payload))
        return response
