from sqlalchemy import Column, Integer, String
from .base import Base

class CrawlConfig(Base):
    __tablename__ = "crawl_config"

    id = Column(Integer, primary_key=True, index=True)
    urls = Column(String)  # JSON-encoded list
    file_types = Column(String)  # CSV or JSON-encoded list
    schedule = Column(String)
