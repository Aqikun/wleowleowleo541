# Lokasi file: src/domains/users/schemas.py
# PERBAIKAN FINAL: Menambahkan kembali skema 'Token' yang hilang

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal, Optional
import enum

# --- Skema BARU yang ditambahkan kembali ---
class Token(BaseModel):
    """Skema untuk respons token JWT."""
    access_token: str
    token_type: str

class UserRole(str, enum.Enum):
    Owner = "Owner"
    Admin = "Admin"
    Kasir = "Kasir"

class UserBase(BaseModel):
    username: str
    email: EmailStr 
    role: UserRole

class UserCreate(UserBase):
    password: str
    phone_number: Optional[str] = None

class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    phone_number: Optional[str] = None

# --- Skema untuk Fitur Lupa Password (Tetap Ada) ---
class ForgotPasswordRequest(BaseModel):
    """Skema untuk permintaan lupa sandi."""
    email: EmailStr
    channel: Literal['email', 'whatsapp']

class ResetPassword(BaseModel):
    """Skema untuk melakukan reset sandi."""
    token: str
    new_password: str