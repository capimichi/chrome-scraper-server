import asyncio
import os

from websockets.server import serve
from websockets.exceptions import ConnectionClosedError

from chromescraperserver.Enum.ConnectionTypeEnum import ConnectionTypeEnum
from chromescraperserver.Handler.WebSocketHandler import WebSocketHandler
from chromescraperserver.Model.IdentifyMessage import IdentifyMessage

host = os.environ.get('HOST', '0.0.0.0')
port = int(os.environ.get('PORT', '8765'))

async def main():

    web_socket_handler = WebSocketHandler()

    async with serve(web_socket_handler.handle, host, port):
        await asyncio.Future()  # run forever


asyncio.run(main())
