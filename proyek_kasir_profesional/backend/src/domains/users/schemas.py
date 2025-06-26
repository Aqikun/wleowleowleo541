# backend/src/domains/users/schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

# # --- Skema Dasar Pengguna ---
# # Berisi field yang umum dan aman untuk ditampilkan.
class UserBase(BaseModel):
    username: str
    
# # --- Skema untuk Membuat Pengguna Baru ---
# # Digunakan saat menerima data registrasi dari API.
class UserCreate(UserBase):
    password: str
    role: str = "Kasir"

# # --- Skema untuk Menampilkan Data Pengguna ---
# # Ini adalah "KTP" yang aman untuk dikirim kembali melalui API.
# # Tidak ada field password di sini untuk keamanan.
class User(UserBase):
    id: int
    role: str

    # # Konfigurasi ini memberitahu Pydantic untuk membaca data
    # # bahkan jika itu bukan dict, tetapi objek ORM (model SQLAlchemy).
    model_config = ConfigDict(from_attributes=True)

