# backend/src/domains/users/schemas.py

from pydantic import BaseModel, ConfigDict
import enum

# # Langkah 1: Definisikan UserRole di sini, bukan di models.py
class UserRole(str, enum.Enum):
    Owner = "Owner"
    Admin = "Admin"
    Kasir = "Kasir"

# # Langkah 2: Hapus baris 'from .models import UserRole' karena sudah didefinisikan di atas.

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    hashed_password: str

class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int