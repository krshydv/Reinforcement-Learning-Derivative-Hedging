import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.websocket.manager import WebSocketManager

configure_logging()
app = FastAPI(title=settings.app_name, openapi_url=f"{settings.api_v1_str}/openapi.json", default_response_class=ORJSONResponse)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RateLimitMiddleware)
app.include_router(api_router, prefix=settings.api_v1_str)
app.state.websocket_manager = WebSocketManager()
logger = structlog.get_logger()

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
