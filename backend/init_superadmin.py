from sqlalchemy.orm import Session
from database import SessionLocal
from models import AdminUser
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_super_admin():
    db: Session = SessionLocal()
    existing = db.query(AdminUser).filter(AdminUser.username == "admin").first()
    
    if existing:
        print("✅ Admin đã tồn tại.")
        return

    admin = AdminUser(
        username="admin",
        password_hash=pwd_context.hash("admin123"),
        role="superadmin"
    )
    db.add(admin)
    db.commit()
    db.close()
    print("✅ Đã tạo tài khoản Super Admin!")

if __name__ == "__main__":
    create_super_admin()
