from __future__ import annotations
import base64
import zlib
import uuid
from datetime import datetime, timezone
from typing import Iterable
import orjson
from redis import Redis as SyncRedis
from redis.asyncio import Redis
from app.schemas.telemetry import TelemetryEvent, TelemetryEventIn


class TelemetryGateway:
    def __init__(self, redis: Redis, buffer_size: int = 500) -> None:
        self.redis = redis
        self.buffer_size = buffer_size

    @classmethod
    def create(cls, redis_url: str, buffer_size: int = 500) -> "TelemetryGateway":
        redis = Redis.from_url(redis_url, decode_responses=True)
        return cls(redis, buffer_size=buffer_size)

    async def publish(self, event: TelemetryEvent) -> None:
        raw = self.serialize(event)
        await self.redis.publish(event.channel, raw)
        key = self._buffer_key(event.channel)
        pipeline = self.redis.pipeline()
        pipeline.lpush(key, raw)
        pipeline.ltrim(key, 0, self.buffer_size - 1)
        await pipeline.execute()

    async def emit(self, payload: TelemetryEventIn, user_id: str | None = None) -> TelemetryEvent:
        event = TelemetryEvent(
            id=str(uuid.uuid4()),
            channel=payload.channel,
            event_type=payload.event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload.payload,
            source=payload.source,
            run_id=payload.run_id,
            user_id=user_id,
        )
        await self.publish(event)
        return event

    async def replay(self, channel: str, limit: int = 100) -> list[TelemetryEvent]:
        key = self._buffer_key(channel)
        raw_items = await self.redis.lrange(key, 0, max(0, limit - 1))
        events = [self.deserialize(item) for item in raw_items]
        return list(reversed(events))

    async def channels(self, prefix: str = "telemetry:") -> list[str]:
        keys = await self.redis.keys(f"{prefix}*")
        return [key.replace(prefix, "") for key in keys]

    async def close(self) -> None:
        await self.redis.aclose()

    @staticmethod
    def serialize(event: TelemetryEvent) -> str:
        return orjson.dumps(event.model_dump(), option=orjson.OPT_SERIALIZE_NUMPY).decode()

    @staticmethod
    def deserialize(raw: str) -> TelemetryEvent:
        return TelemetryEvent.model_validate(orjson.loads(raw))

    @staticmethod
    def compress(payload: dict) -> dict:
        encoded = orjson.dumps(payload, option=orjson.OPT_SERIALIZE_NUMPY)
        compressed = base64.b64encode(zlib.compress(encoded)).decode()
        return {"compressed": True, "data": compressed}

    @staticmethod
    def decompress(payload: dict) -> dict:
        if payload.get("compressed"):
            data = base64.b64decode(payload["data"])
            return orjson.loads(zlib.decompress(data))
        return payload

    @staticmethod
    def _buffer_key(channel: str) -> str:
        return f"telemetry:{channel}"


class SyncTelemetryPublisher:
    def __init__(self, redis: SyncRedis, buffer_size: int = 500) -> None:
        self.redis = redis
        self.buffer_size = buffer_size

    @classmethod
    def create(cls, redis_url: str, buffer_size: int = 500) -> "SyncTelemetryPublisher":
        redis = SyncRedis.from_url(redis_url, decode_responses=True)
        return cls(redis, buffer_size=buffer_size)

    def publish(self, event: TelemetryEvent) -> None:
        raw = TelemetryGateway.serialize(event)
        self.redis.publish(event.channel, raw)
        key = TelemetryGateway._buffer_key(event.channel)
        pipeline = self.redis.pipeline()
        pipeline.lpush(key, raw)
        pipeline.ltrim(key, 0, self.buffer_size - 1)
        pipeline.execute()

    def emit(self, payload: TelemetryEventIn, user_id: str | None = None) -> TelemetryEvent:
        event = TelemetryEvent(
            id=str(uuid.uuid4()),
            channel=payload.channel,
            event_type=payload.event_type,
            timestamp=datetime.now(timezone.utc),
            payload=payload.payload,
            source=payload.source,
            run_id=payload.run_id,
            user_id=user_id,
        )
        self.publish(event)
        return event

    def close(self) -> None:
        self.redis.close()


def normalize_channels(channels: str | Iterable[str] | None) -> list[str]:
    if not channels:
        return []
    if isinstance(channels, str):
        return [item.strip() for item in channels.split(",") if item.strip()]
    return [item.strip() for item in channels if item.strip()]
