from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class TrainedDocument(Base):
    __tablename__ = "trained_documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    source = Column(String, nullable=False)  # upload, crawl, etc
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)