from openai import OpenAI
from sqlalchemy.orm import Session
from services.config_service import get_config

_cached_client = None

def get_openai_client(db: Session) -> OpenAI:
    global _cached_client
    if _cached_client is not None:
        return _cached_client

    api_key = get_config(db, "openai_key")
    if not api_key:
        raise ValueError("⚠️ Chưa cấu hình OpenAI API Key trong AppConfig")

    _cached_client = OpenAI(api_key=api_key)
    return _cached_client
