from sqlalchemy.orm import Session
from models import config_model

def get_config(db: Session, key: str) -> str | None:
    result = db.query(Config).filter(Config.key == key).first()
    return result.value if result else None

def set_config(db: Session, key: str, value: str):
    config = db.query(Config).filter(Config.key == key).first()
    if config:
        config.value = value
    else:
        config = Config(key=key, value=value)
        db.add(config)
    db.commit()