from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services import config_service
from services.config_service import get_all_configs


router = APIRouter(prefix="/api/config", tags=["Config"])

@router.get("/{key}", response_model=str)
def get_config_value(key: str, db: Session = Depends(get_db)):
    value = config_service.get_config(db, key)
    if value is None:
        raise HTTPException(status_code=404, detail="Config not found")
    return value

@router.post("/")
def set_config_value(key: str, value: str, db: Session = Depends(get_db)):
    config_service.set_config(db, key, value)
    return {"message": "Config saved successfully"}

@router.get("/", response_model=dict)
def get_all_configs(db: Session = Depends(get_db)):
    return config_service.get_all_configs(db) 

@router.delete("/{key}")
def delete_config_value(key: str, db: Session = Depends(get_db)):
    success = config_service.delete_config(db, key)
    if not success:
        raise HTTPException(status_code=404, detail="Config not found")
    return {"message": "Config deleted successfully"}
