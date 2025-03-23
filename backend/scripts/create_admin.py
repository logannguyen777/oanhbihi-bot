from database import SessionLocal
from models import AdminUser
from passlib.hash import bcrypt

db = SessionLocal()
admin = AdminUser(
    username="admin",
    password_hash=bcrypt.hash("oanhbihi"),
    role="superadmin"
)
db.add(admin)
db.commit()
