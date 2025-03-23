from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import os

router = APIRouter(
    prefix="/zalo",
    tags=["zalo"]
)

VERIFY_TOKEN = os.getenv("ZALO_VERIFY_TOKEN", "zalo_secret")

@router.post("/webhook")
async def zalo_webhook(request: Request):
    body = await request.json()
    
    # Xác thực verify token nếu có
    if "data" not in body:
        raise HTTPException(status_code=400, detail="Invalid Zalo payload")

    # TODO: Xử lý tin nhắn nhận được từ Zalo
    # Ví dụ: in ra log
    print("Zalo message received:", body["data"])

    return JSONResponse(content={"message": "received"}, status_code=200)
