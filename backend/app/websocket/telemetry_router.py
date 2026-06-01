from __future__ import annotations

import asyncio
from typing import Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from prometheus_client import Counter, Gauge
from app.services.auth_service import authenticate_websocket_token
from app.services.telemetry_service import TelemetryGateway, normalize_channels

router = APIRouter()

telemetry_connections = Gauge("telemetry_ws_connections", "Active telemetry websocket connections")
telemetry_messages = Counter("telemetry_ws_messages", "Telemetry websocket messages sent", ["channel"])
telemetry_errors = Counter("telemetry_ws_errors", "Telemetry websocket errors")


async def _send_loop(websocket: WebSocket, queue: asyncio.Queue) -> None:
    while True:
        message = await queue.get()
        await websocket.send_json(message)


@router.websocket("/ws/telemetry")
async def telemetry_socket(websocket: WebSocket):
    gateway: TelemetryGateway = websocket.app.state.telemetry
    token = websocket.query_params.get("token")
    channels = set(normalize_channels(websocket.query_params.get("channels")))
    replay = int(websocket.query_params.get("replay", "0"))
    compress = websocket.query_params.get("compress") == "1"

    await websocket.accept()
    try:
        await authenticate_websocket_token(token)
    except Exception:
        await websocket.close(code=4401)
        return

    telemetry_connections.inc()
    queue: asyncio.Queue = asyncio.Queue(maxsize=200)

    async def enqueue(message: dict) -> None:
        try:
            queue.put_nowait(message)
        except asyncio.QueueFull:
            try:
                _ = queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            queue.put_nowait(message)
    sender_task = asyncio.create_task(_send_loop(websocket, queue))
    pubsub = gateway.redis.pubsub()

    async def subscribe(selected: set[str]) -> None:
        if not selected:
            return
        await pubsub.subscribe(*selected)

    async def unsubscribe(selected: set[str]) -> None:
        if not selected:
            return
        await pubsub.unsubscribe(*selected)

    async def handle_client_messages() -> None:
        nonlocal channels
        while True:
            payload = await websocket.receive_json()
            msg_type = payload.get("type")
            if msg_type == "subscribe":
                new_channels = set(normalize_channels(payload.get("channels")))
                added = new_channels - channels
                if added:
                    await subscribe(added)
                channels |= new_channels
            if msg_type == "unsubscribe":
                remove_channels = set(normalize_channels(payload.get("channels")))
                if remove_channels:
                    await unsubscribe(remove_channels)
                channels -= remove_channels
            if msg_type == "ping":
                await enqueue({"type": "pong"})

    client_task = asyncio.create_task(handle_client_messages())

    try:
        await subscribe(channels)
        if replay and channels:
            for channel in channels:
                events = await gateway.replay(channel, limit=replay)
                for event in events:
                    payload = event.model_dump(mode="json")
                    message = TelemetryGateway.compress(payload) if compress else payload
                    await enqueue(message)
                    telemetry_messages.labels(channel=channel).inc()

        while True:
            try:
                message: dict[str, Any] | None = await pubsub.get_message(ignore_subscribe_messages=True, timeout=20)
                if message is None:
                    await enqueue({"type": "ping"})
                    continue
                raw = message.get("data")
                event = gateway.deserialize(raw)
                payload = event.model_dump(mode="json")
                output = TelemetryGateway.compress(payload) if compress else payload
                await enqueue(output)
                telemetry_messages.labels(channel=event.channel).inc()
            except asyncio.CancelledError:
                raise
            except Exception:
                telemetry_errors.inc()
    except WebSocketDisconnect:
        pass
    except Exception:
        telemetry_errors.inc()
    finally:
        sender_task.cancel()
        client_task.cancel()
        await pubsub.close()
        telemetry_connections.dec()
