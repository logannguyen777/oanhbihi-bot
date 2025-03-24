from sqlalchemy.orm import Session
from models import BotPersona

def get_personas(db: Session):
    return db.query(BotPersona).all()

def get_persona_by_id(db: Session, persona_id: int):
    return db.query(BotPersona).filter(BotPersona.id == persona_id).first()

def create_or_update_persona(db: Session, data: dict):
    persona = None
    if "id" in data:
        persona = db.query(BotPersona).filter(BotPersona.id == data["id"]).first()
    if persona:
        for k, v in data.items():
            setattr(persona, k, v)
    else:
        persona = BotPersona(**data)
        db.add(persona)
    db.commit()
    return persona