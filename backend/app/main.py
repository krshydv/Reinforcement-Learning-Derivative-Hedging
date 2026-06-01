from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
import structlog
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.telemetry import TelemetryMiddleware
from app.websocket.manager import WebSocketManager
from app.services.seed_service import SeedService
from app.websocket.router import router as ws_router
from app.websocket.telemetry_router import router as telemetry_ws_router
from app.services.telemetry_service import TelemetryGateway

configure_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.websocket_manager = WebSocketManager()
    app.state.telemetry = TelemetryGateway.create(settings.redis_url)
    await SeedService().seed()
    yield
    await app.state.websocket_manager.close_all()
    await app.state.telemetry.close()

origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

app = FastAPI(title=settings.app_name, openapi_url=f"{settings.api_v1_str}/openapi.json", default_response_class=ORJSONResponse, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"], allow_headers=["Authorization", "Content-Type"])
app.add_middleware(RateLimitMiddleware)
app.add_middleware(TelemetryMiddleware)
app.include_router(api_router, prefix=settings.api_v1_str)
app.include_router(ws_router)
app.include_router(telemetry_ws_router)
logger = structlog.get_logger()

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
