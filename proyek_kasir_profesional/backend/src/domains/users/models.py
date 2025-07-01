# Lokasi file: src/domains/users/models.py
# PENAMBAHAN: Kolom 'force_password_reset'.

from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.sql import func
from src.core.database import Base
# Ganti impor ini untuk menghindari circular import saat Alembic berjalan
from .schemas import UserRole as UserRoleSchema

class User(Base):
    """
    Model Database untuk tabel 'users'.
    Ini adalah cetak biru untuk data pengguna yang disimpan di database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- Kolom Identitas & Kontak ---
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)

    # --- Kolom Keamanan & Peran ---
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRoleSchema), nullable=False, server_default=UserRoleSchema.Kasir.name)
    
    # --- Kolom Status Akun ---
    is_active = Column(Boolean, default=True, nullable=False)
    # # Kolom BARU untuk memaksa reset password
    force_password_reset = Column(Boolean, default=False, nullable=False)
    
    # --- Kolom untuk Fitur Lupa Password ---
    reset_token = Column(String, nullable=True, unique=True) 
    reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # --- Kolom Pelacakan Waktu (Audit Timestamps) ---
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())