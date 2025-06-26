# backend/src/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Membuat engine SQLAlchemy untuk koneksi ke database.
# URL diambil dari file .env melalui objek settings.
engine = create_engine(
    settings.DATABASE_URL,
    # Opsi connect_args ini khusus untuk SQLite.
    # Untuk PostgreSQL atau MySQL, Anda bisa menghapusnya.
    connect_args={"check_same_thread": False} 
)

# Membuat pabrik sesi (session factory)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Membuat kelas dasar (Base) untuk semua model ORM.
# Semua tabel model kita akan mewarisi dari kelas ini.
Base = declarative_base()

# Fungsi dependency untuk menyediakan sesi database ke setiap endpoint API.
# Ini adalah pola standar di FastAPI untuk manajemen sesi.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
