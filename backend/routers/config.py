from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from services import config_service
from models.config_model import AppConfig  # Nhớ import nếu chưa có
from typing import Optional

router = APIRouter(prefix="/config", tags=["Config"])

# 🔹 Lấy giá trị config theo key
@router.get("/{key}", response_model=str)
def get_config_value(key: str, db: Session = Depends(get_db)):
    value = config_service.get_config(db, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return value

# 🔹 Lấy toàn bộ config
@router.get("", response_model=dict)
def get_all_configs(db: Session = Depends(get_db)):
    return config_service.get_all_configs(db)

# 🔹 Tạo hoặc cập nhật config
@router.post("")
def set_config(
    key: str = Query(...),
    value: str = Query(...),
    db: Session = Depends(get_db)
):
    config = db.query(AppConfig).filter(AppConfig.key == key).first()
    if config:
        config.value = value
    else:
        config = AppConfig(key=key, value=value)
        db.add(config)
    db.commit()
    return {"message": f"✅ Đã lưu cấu hình '{key}' thành công!"}

# 🔹 Xoá config theo key
@router.delete("/{key}")
def delete_config_value(key: str, db: Session = Depends(get_db)):
    success = config_service.delete_config(db, key)
    if not success:
        raise HTTPException(status_code=404, detail="Config not found")
    return {"message": f"🗑️ Đã xoá cấu hình '{key}'"}
