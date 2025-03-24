from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from uuid import uuid4

from .base import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536), nullable=True)

    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    document = relationship("Document", back_populates="chunks")