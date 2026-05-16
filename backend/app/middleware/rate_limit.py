from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
import redis.asyncio as redis

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rate = settings.rate_limit
        try:
            limit_text, window_text = rate.split("/")
            limit = int(limit_text)
        except ValueError:
            return await call_next(request)
        window_unit = window_text.lower()
        if window_unit.startswith("sec"):
            window_seconds = 1
        elif window_unit.startswith("min"):
            window_seconds = 60
        elif window_unit.startswith("hour"):
            window_seconds = 3600
        else:
            return await call_next(request)
        r = None
        try:
            r = redis.from_url(settings.redis_url)
            host = request.client.host if request.client else "unknown"
            key = f"rate:{host}"
            current = await r.incr(key)
            if current == 1:
                await r.expire(key, window_seconds)
            if current > limit:
                return Response(status_code=429)
        except Exception:
            return await call_next(request)
        finally:
            if r is not None:
                await r.close()
        return await call_next(request)
