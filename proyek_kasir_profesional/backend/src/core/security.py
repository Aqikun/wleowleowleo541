# Lokasi file: src/core/security.py
# PERBARUAN: Menambahkan fungsi untuk membuat token reset yang aman

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
import secrets # Modul standar Python untuk menghasilkan token yang aman secara kriptografis

# --- Konfigurasi Hashing Password (Tetap Sama) ---
# Menggunakan bcrypt, algoritma yang kuat dan standar industri
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Konfigurasi JSON Web Token (JWT) untuk Login (Tetap Sama) ---
# Kunci rahasia ini HARUS diganti dengan nilai acak yang kuat di lingkungan produksi
# Anda bisa membuatnya dengan `openssl rand -hex 32`
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Memverifikasi password mentah dengan hash yang ada di database."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Mengubah password mentah menjadi hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Membuat access token JWT untuk sesi login."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Fungsi Keamanan BARU untuk Fitur Lupa Password ---

def create_reset_token() -> str:
    """
    Membuat token URL-safe yang acak dan aman secara kriptografis.
    Token ini akan dikirim ke pengguna.
    """
    # Menghasilkan 32 byte acak dan mengonversinya menjadi format heksadesimal yang aman untuk URL
    return secrets.token_hex(32)
