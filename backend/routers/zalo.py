from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services.config_service import get_config
from database import get_db

router = APIRouter(prefix="/zalo", tags=["zalo"])

@router.post("/webhook")
async def zalo_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    VERIFY_TOKEN = get_config(db, "zalo_verify_token")

    if "data" not in body:
        raise HTTPException(status_code=400, detail="Invalid Zalo payload")

    print("Zalo message received:", body["data"])
    return JSONResponse(content={"message": "received"}, status_code=200)