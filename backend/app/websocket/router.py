from fastapi import APIRouter, WebSocket
from app.main import app

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    manager = app.state.websocket_manager
    await manager.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except Exception:
        await manager.disconnect(client_id)
