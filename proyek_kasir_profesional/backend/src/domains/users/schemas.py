# Lokasi file: src/domains/users/schemas.py
# PENAMBAHAN: Field 'force_password_reset'.

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal, Optional
import enum

# --- Skema Otentikasi & Peran ---
class Token(BaseModel):
    access_token: str
    token_type: str

class UserRole(str, enum.Enum):
    Owner = "Owner"
    Admin = "Admin"
    Kasir = "Kasir"

# --- Skema Pengguna ---
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
    is_active: bool
    force_password_reset: bool # <-- Tambahkan field ini

# --- Skema untuk Update ---
class UserStatusUpdate(BaseModel):
    is_active: bool

class UserRoleUpdate(BaseModel):
    role: UserRole

# --- Skema untuk Fitur Lupa Password ---
class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    channel: Literal['email', 'whatsapp']

class ResetPassword(BaseModel):
    token: str
    new_password: str