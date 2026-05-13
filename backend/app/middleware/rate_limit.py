from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
import redis.asyncio as redis
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        r = redis.from_url(settings.redis_url)
        key = f"rate:{request.client.host}"
        current = await r.get(key)
        limit = int(settings.rate_limit.split("/")[0])
        if current and int(current) >= limit:
            return Response(status_code=429)
        await r.incr(key)
        await r.expire(key, 60)
        return await call_next(request)
