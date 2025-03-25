from sqlalchemy import Column, Integer, String
from .base import Base

class WebPage(Base):
    __tablename__ = "web_pages"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    content = Column(String)
    embedding = Column(String)  # Trường lưu vector dạng JSON hoặc array
    chunk_count = Column(Integer, default=0)
