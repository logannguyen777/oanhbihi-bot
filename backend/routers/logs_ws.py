from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
active_connections: list[WebSocket] = []

@router.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # giữ kết nối
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def broadcast_log(message: str):
    for conn in active_connections:
        try:
            await conn.send_text(message)
        except:
            continue