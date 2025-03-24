from sqlalchemy.orm import Session
from models.config_model import AppConfig


def get_config(db: Session, key: str) -> str | None:
    config = db.query(AppConfig).filter(AppConfig.key == key).first()
    return config.value if config else None


def set_config(db: Session, key: str, value: str) -> None:
    config = db.query(AppConfig).filter(AppConfig.key == key).first()
    if config:
        config.value = value
    else:
        config = AppConfig(key=key, value=value)
        db.add(config)
    db.commit()

def get_all_configs(db: Session) -> dict[str, str]:
    configs = db.query(AppConfig).all()
    return {c.key: c.value for c in configs}

def delete_config(db: Session, key: str) -> bool:
    config = db.query(AppConfig).filter(AppConfig.key == key).first()
    if config:
        db.delete(config)
        db.commit()
        return True
    return False
