from dataclasses import dataclass
from typing import Dict
import asyncio
from fastapi import WebSocket


@dataclass
class ClientConnection:
    websocket: WebSocket
    queue: asyncio.Queue
    sender_task: asyncio.Task
    last_seen: float

class WebSocketManager:
    def __init__(self) -> None:
        self.connections: Dict[str, ClientConnection] = {}
        self.queue_maxsize = 100
        self.send_timeout = 2.0

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        queue: asyncio.Queue = asyncio.Queue(maxsize=self.queue_maxsize)
        sender_task = asyncio.create_task(self._sender_loop(client_id, websocket, queue))
        self.connections[client_id] = ClientConnection(
            websocket=websocket,
            queue=queue,
            sender_task=sender_task,
            last_seen=asyncio.get_running_loop().time(),
        )

    async def disconnect(self, client_id: str) -> None:
        connection = self.connections.pop(client_id, None)
        if connection:
            connection.sender_task.cancel()
            try:
                await connection.websocket.close()
            except Exception:
                pass

    async def broadcast(self, message: dict) -> None:
        for connection in list(self.connections.values()):
            await self._enqueue(connection, message)

    async def close_all(self) -> None:
        for client_id in list(self.connections.keys()):
            await self.disconnect(client_id)

    async def touch(self, client_id: str) -> None:
        connection = self.connections.get(client_id)
        if connection:
            connection.last_seen = asyncio.get_running_loop().time()

    async def send_to(self, client_id: str, message: dict) -> None:
        connection = self.connections.get(client_id)
        if connection:
            await self._enqueue(connection, message)

    async def _enqueue(self, connection: ClientConnection, message: dict) -> None:
        try:
            connection.queue.put_nowait(message)
        except asyncio.QueueFull:
            try:
                _ = connection.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            connection.queue.put_nowait(message)

    async def _sender_loop(self, client_id: str, websocket: WebSocket, queue: asyncio.Queue) -> None:
        while True:
            message = await queue.get()
            try:
                await asyncio.wait_for(websocket.send_json(message), timeout=self.send_timeout)
            except Exception:
                await self.disconnect(client_id)
                return
