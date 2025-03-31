from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://chatbot_user:secretpassword@oanhbihi-postgres:5432/chatbot_db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ✅ Đây là hàm bị thiếu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()