from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import get_db
from models import BotPersona
from services.persona_service import get_personas, get_persona_by_id, create_or_update_persona

router = APIRouter(prefix="/persona", tags=["persona"])

class PersonaIn(BaseModel):
    name: str
    age: int
    style: str
    prompt: str

@router.get("", response_model=List[PersonaIn])
def list_personas(db: Session = Depends(get_db)):
    return db.query(BotPersona).all()

@router.post("")
def create_persona(data: PersonaIn, db: Session = Depends(get_db)):
    persona = BotPersona(**data.dict())
    db.add(persona)
    db.commit()
    return {"message": "✅ Đã tạo persona mới!"}

@router.delete("/{persona_id}")
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(BotPersona).filter(BotPersona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Không tìm thấy persona")
    db.delete(persona)
    db.commit()
    return {"message": "🗑️ Đã xoá persona"}