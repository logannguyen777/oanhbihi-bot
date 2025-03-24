from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import config_model
from services.config_service import get_config, set_config

router = APIRouter(prefix="/api/config", tags=["config"])

@router.get("")
def get_config_api(
    key: str = Query(None),
    db: Session = Depends(get_db)
):
    if key:
        value = get_config(db, key)
        if value is None:
            raise HTTPException(status_code=404, detail="Config not found")
        return {"key": key, "value": value}
    return get_all_configs(db)

@router.post("")
def set_config_api(
    body: dict,
    db: Session = Depends(get_db)
):
    key = body.get("key")
    value = body.get("value")
    if not key or value is None:
        raise HTTPException(status_code=400, detail="Key and value are required")
    set_config(db, key, value)
    return {"message": f"✅ Đã cập nhật cấu hình `{key}` thành công!"}