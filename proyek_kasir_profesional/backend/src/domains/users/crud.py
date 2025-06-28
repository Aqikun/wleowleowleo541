# Lokasi file: backend/src/domains/users/crud.py
# # Versi final yang sudah diperbaiki

from sqlalchemy.orm import Session
from src.core.security import get_password_hash
from . import models, schemas

def get_user_by_username(db: Session, username: str):
    # # Mengambil data satu user dari database berdasarkan username.
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # # Membuat user baru di database.
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        # # PERBAIKAN: Gunakan .value untuk mendapatkan nilai string dari Enum
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# # Pastikan fungsi-fungsi lain yang mungkin dibutuhkan juga ada
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def count_users(db: Session) -> int:
    return db.query(models.User).count()