# backend/src/domains/users/models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.core.database import Base

class User(Base):
    # # Nama tabel di database nanti adalah 'users'
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="Kasir")

    # # Menambahkan hubungan ke tabel Transaction
    transactions = relationship("Transaction", back_populates="cashier")
