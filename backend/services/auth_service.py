from sqlalchemy.orm import Session
from models import AdminUser
from passlib.hash import bcrypt

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if user and bcrypt.verify(password, user.password_hash):
        return user
    return None

def create_admin_user(db: Session, username: str, password: str, role="admin"):
    from datetime import datetime
    from models.enum import RoleEnum
    hashed_pw = bcrypt.hash(password)
    user = AdminUser(username=username, password_hash=hashed_pw, role=RoleEnum(role), created_at=datetime.utcnow())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user