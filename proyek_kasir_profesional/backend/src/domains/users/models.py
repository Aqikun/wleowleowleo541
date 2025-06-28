# Lokasi file: src/domains/users/models.py
# Versi final dengan tambahan kolom untuk email, no. telp, & reset password

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.sql import func
from src.core.database import Base
from src.domains.users.schemas import UserRole 

class User(Base):
    """
    Model Database untuk tabel 'users'.
    Ini adalah cetak biru untuk data pengguna yang disimpan di database.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- Kolom Identitas & Kontak ---
    username = Column(String, unique=True, index=True, nullable=False)
    # Email wajib ada, untuk otentikasi dan komunikasi
    email = Column(String, unique=True, index=True, nullable=False)
    # Nomor telepon (opsional), untuk notifikasi WhatsApp
    phone_number = Column(String, unique=True, index=True, nullable=True)

    # --- Kolom Keamanan & Peran ---
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, server_default=UserRole.Kasir.name)
    
    # --- Kolom untuk Fitur Reset Password ---
    # Menyimpan hash dari token, bukan token aslinya
    reset_token = Column(String, nullable=True, unique=True) 
    # Menyimpan waktu kedaluwarsa token
    reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # --- Kolom Pelacakan Waktu (Audit Timestamps) ---
    # Dicatat otomatis saat user pertama kali dibuat
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Diperbarui otomatis setiap kali ada perubahan pada data user
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())