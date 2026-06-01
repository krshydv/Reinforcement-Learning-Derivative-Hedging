import pytest
from app.core.config import settings
from app.schemas.telemetry import TelemetryEventIn
from app.services.telemetry_service import TelemetryGateway


@pytest.mark.asyncio
@pytest.mark.integration
async def test_telemetry_publish_and_replay():
    try:
        gateway = TelemetryGateway.create(settings.redis_url, buffer_size=10)
    except Exception as exc:
        pytest.skip(f"redis unavailable: {exc}")
    await gateway.redis.delete("telemetry:test")
    event = await gateway.emit(TelemetryEventIn(channel="test", event_type="unit", payload={"value": 42}), user_id="tester")
    replay = await gateway.replay("test", limit=5)
    await gateway.redis.delete("telemetry:test")
    await gateway.close()
    assert replay
    assert replay[-1].id == event.id
    assert replay[-1].payload["value"] == 42


def test_telemetry_compression_roundtrip():
    payload = {"metric": 1.23, "status": "ok"}
    compressed = TelemetryGateway.compress(payload)
    decompressed = TelemetryGateway.decompress(compressed)
    assert decompressed == payload
