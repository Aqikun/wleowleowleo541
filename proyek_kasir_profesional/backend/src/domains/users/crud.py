# Lokasi file: src/domains/users/crud.py
# PERBARUAN: Menambahkan logika untuk fitur Lupa Password & menyesuaikan create_user

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.core.security import get_password_hash
from . import models, schemas

# --- Fungsi CRUD yang sudah ada (dengan modifikasi) ---

def get_user_by_username(db: Session, username: str):
    """Mencari pengguna berdasarkan username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Membuat pengguna baru dengan data kontak.
    Fungsi ini sekarang menangani email dan nomor telepon.
    """
    hashed_password = get_password_hash(user.password)
    # Membuat objek User baru dengan semua field yang diperlukan dari skema
    db_user = models.User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number, # Menyimpan nomor telepon (jika ada)
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Fungsi CRUD BARU untuk Fitur Lupa Password ---

def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Mencari pengguna berdasarkan alamat email."""
    return db.query(models.User).filter(models.User.email == email).first()

def set_password_reset_token(db: Session, user: models.User, token: str) -> models.User:
    """
    Menyimpan HASH dari token reset dan waktu kedaluwarsanya ke database.
    """
    # Menetapkan waktu kedaluwarsa, misalnya 15 menit dari sekarang
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    
    user.reset_token = token # Ingat, ini adalah HASH dari token, bukan token asli
    user.reset_token_expires_at = expires_at
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_reset_token(db: Session, token: str) -> models.User | None:
    """Mencari pengguna berdasarkan HASH token reset yang valid."""
    return (
        db.query(models.User)
        .filter(models.User.reset_token == token)
        # Pastikan token belum kedaluwarsa
        .filter(models.User.reset_token_expires_at > datetime.utcnow())
        .first()
    )

def update_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    """
    Memperbarui password pengguna dan menghapus token reset.
    """
    user.hashed_password = get_password_hash(new_password)
    # Menghapus token setelah berhasil digunakan untuk keamanan
    user.reset_token = None
    user.reset_token_expires_at = None
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user