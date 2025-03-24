from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models import * 
from database import DATABASE_URL, get_db

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    print("📦 Đang tạo các bảng trong database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tạo bảng xong rồi nha!")
