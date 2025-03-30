from pydantic import BaseModel
from uuid import UUID

class FacebookPageCreate(BaseModel):
    page_id: str
    page_name: str
    access_token: str
    agent_id: UUID
