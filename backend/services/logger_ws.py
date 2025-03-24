from routers.logs_ws import active_connections

async def broadcast_log(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            pass
