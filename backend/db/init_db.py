from sqlalchemy import create_engine
from models import Base  # import Base từ models/__init__.py
from models.user import User  # import từng model bạn có

from database import SQLALCHEMY_DATABASE_URL  # Đường kết nối DB của bạn

def init_db():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
