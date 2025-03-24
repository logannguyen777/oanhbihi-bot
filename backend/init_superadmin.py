# 📁 init_superadmin.py
from sqlalchemy.orm import Session
from database import SessionLocal
from models import AdminUser, RoleEnum
from datetime import datetime
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_super_admin():
    db: Session = SessionLocal()
    try:
        existing = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if existing:
            print("⚠️ Super admin 'admin' đã tồn tại.")
            return

        admin = AdminUser(
            username="admin",
            password_hash=hash_password("admin123"),
            role=RoleEnum.superadmin,
            created_at=datetime.utcnow(),
        )
        db.add(admin)
        db.commit()
        print("✅ Super admin mặc định đã được tạo: admin / admin123")
    finally:
        db.close()


if __name__ == "__main__":
    create_super_admin()
