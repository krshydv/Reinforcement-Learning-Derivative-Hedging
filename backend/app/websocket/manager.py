from typing import Dict
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self) -> None:
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[client_id] = websocket

    async def disconnect(self, client_id: str) -> None:
        if client_id in self.connections:
            await self.connections[client_id].close()
            del self.connections[client_id]

    async def broadcast(self, message: dict) -> None:
        for ws in self.connections.values():
            await ws.send_json(message)
