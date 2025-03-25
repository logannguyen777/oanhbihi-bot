from pydantic import BaseModel
from typing import Optional, Literal

class ChatRequest(BaseModel):
    sender_id: str
    channel: Literal["messenger", "zalo", "web"]
    message: str
    session_id: Optional[str] = None

class ChatRagRequest(BaseModel):
    sender_id: str
    channel: Literal["messenger", "zalo", "web"]
    message: str
    session_id: Optional[str] = None
    top_k: Optional[int] = 3

class ChatResponse(BaseModel):
    message: str
    session_id: Optional[str]