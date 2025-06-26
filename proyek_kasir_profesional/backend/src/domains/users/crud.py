# backend/src/domains/users/crud.py
from sqlalchemy.orm import Session

# Pastikan kita mengimpor security untuk hashing password
from src.core.security import get_password_hash
from . import models, schemas

# INI ADALAH FUNGSI YANG HILANG
def get_user_by_username(db: Session, username: str):
    """
    # Mengambil data satu user dari database berdasarkan username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    # Membuat user baru di database.
    # Password mentah di-hash sebelum disimpan.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
