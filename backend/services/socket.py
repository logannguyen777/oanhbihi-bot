# services/socket.py

from fastapi_socketio import SocketManager

sio = None  # <-- tạm để rỗng, sẽ gán trong main.py

def init_socket(app):
    global sio
    sio = SocketManager(app)

    @sio.on("connect")
    async def handle_connect(sid, environ):
        print(f"✨ Client connected: {sid}")

    @sio.on("disconnect")
    async def handle_disconnect(sid):
        print(f"💨 Client disconnected: {sid}")
