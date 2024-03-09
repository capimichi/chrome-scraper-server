import asyncio
import os

import websockets
from websockets.server import serve
from websockets.exceptions import ConnectionClosedError

from chromescraperserver.Enum.ConnectionTypeEnum import ConnectionTypeEnum
from chromescraperserver.Handler.WebSocketHandler import WebSocketHandler
from chromescraperserver.Model.IdentifyMessage import IdentifyMessage
from fastapi import FastAPI
from chromescraperserver.Handler.WebSocketHandler import WebSocketHandler
from chromescraperserver.Model.TaskMessage import TaskMessage
from typing import Optional, Dict, Any, List

host = os.environ.get('HOST', '0.0.0.0')
port = int(os.environ.get('PORT', '8766'))

socket_host = os.environ.get('SOCKET_HOST', '0.0.0.0')
socket_port = int(os.environ.get('SOCKET_PORT', '8765'))


app = FastAPI()
@app.get("/workers")
async def get_workers():
    # connect to the websocket server
    uri = f"ws://{socket_host}:{socket_port}"
    async with websockets.connect(uri) as websocket:
        # send the identify message
        identify_message = IdentifyMessage(type=ConnectionTypeEnum.API_TYPE)
        await websocket.send(identify_message.model_dump_json())
        # receive the response
        response = await websocket.recv()
        return response

@app.post("/tasks/get-page")
async def create_task_get_page():
    worker_connections = await handler.get_worker_connections()
    task_id = str(hash(str(time.time())))
    task_message = TaskMessage(task_id=task_id, operation="GET_PAGE")
    handler.tasks[task_id] = task_message
    worker_connection = worker_connections[0]
    await worker_connection.get_websocket().send(task_message.model_dump_json())
    return {"task_id": task_id}