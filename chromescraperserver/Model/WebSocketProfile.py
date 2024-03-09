from websockets import WebSocketServerProtocol


class WebSocketProfile:
    websocket: WebSocketServerProtocol
    type: str

    def __init__(self, websocket: WebSocketServerProtocol):
        self.websocket = websocket

    def get_websocket(self):
        return self.websocket

    def set_websocket(self, websocket: WebSocketServerProtocol):
        self.websocket = websocket

    def get_type(self):
        return self.type

    def set_type(self, type: str):
        self.type = type

    def is_identified(self):
        return self.type is not None

    def get_connection_key(self):
        return f"{self.websocket.remote_address[0]}:{self.websocket.remote_address[1]}"
