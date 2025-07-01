# Lokasi file: src/domains/users/crud.py
# PERBAIKAN FINAL: Bekerja dengan token asli, bukan hash.

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from src.core.security import get_password_hash
from . import models, schemas

# --- Fungsi Pencarian ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()

# --- FUNGSI INI SEKARANG MENCARI TOKEN ASLI ---
def get_user_by_reset_token(db: Session, token: str) -> models.User | None:
    """Mencari pengguna berdasarkan token reset ASLI yang valid."""
    return (
        db.query(models.User)
        .filter(models.User.reset_token == token) # Mencari token asli
        .filter(models.User.reset_token_expires_at > datetime.now(timezone.utc))
        .first()
    )

# --- Fungsi Pembuatan & Pembaruan ---
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, phone_number=user.phone_number,
        hashed_password=hashed_password, role=user.role, is_active=True,
        force_password_reset=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- FUNGSI INI SEKARANG MENYIMPAN TOKEN ASLI ---
def set_password_reset_token(db: Session, user: models.User, token: str) -> models.User:
    """Menyimpan token reset ASLI dan waktu kedaluwarsanya."""
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    user.reset_token = token # Menyimpan token asli
    user.reset_token_expires_at = expires_at
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires_at = None
    user.force_password_reset = False
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# (Sisa fungsi lain tidak berubah)
def update_user_status(db: Session, db_user: models.User, status_update: schemas.UserStatusUpdate) -> models.User:
    db_user.is_active = status_update.is_active; db.add(db_user); db.commit(); db.refresh(db_user); return db_user
def update_user_role(db: Session, db_user: models.User, role_update: schemas.UserRoleUpdate) -> models.User:
    db_user.role = role_update.role; db.add(db_user); db.commit(); db.refresh(db_user); return db_user
def set_force_password_reset(db: Session, db_user: models.User, status: bool) -> models.User:
    db_user.force_password_reset = status; db.add(db_user); db.commit(); db.refresh(db_user); return db_user