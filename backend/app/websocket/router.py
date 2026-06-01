import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.auth_service import authenticate_websocket_token

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    manager = websocket.app.state.websocket_manager
    token = websocket.query_params.get("token")
    await websocket.accept()
    try:
        await authenticate_websocket_token(token)
    except Exception:
        await websocket.close(code=4401)
        return
    await manager.connect(client_id, websocket)
    try:
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_json(), timeout=25)
            except asyncio.TimeoutError:
                await manager.send_to(client_id, {"type": "ping"})
                continue
            await manager.touch(client_id)
            if isinstance(data, dict) and data.get("type") == "pong":
                continue
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(client_id)
    except Exception:
        await manager.disconnect(client_id)
