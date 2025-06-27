# backend/src/domains/users/models.py

from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.core.database import Base
# # Impor UserRole dari schemas, bukan mendefinisikannya di sini
from .schemas import UserRole

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # # Gunakan UserRole yang sudah diimpor
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.Kasir)