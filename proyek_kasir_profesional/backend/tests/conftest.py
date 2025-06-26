# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# # Impor penting dari proyek kita
from src.core.database import Base, get_db
from src.core.config import settings
from src.main import app

# # Pastikan kita menggunakan database untuk TESTING
SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # Fungsi ini akan menimpa dependency 'get_db' yang asli
# # sehingga semua endpoint API selama tes akan menggunakan database testing.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# # Terapkan penimpaan (override) pada aplikasi FastAPI kita
app.dependency_overrides[get_db] = override_get_db


# # INI ADALAH FIXTURE 'CLIENT' YANG DICARI OLEH PYTEST
@pytest.fixture(scope="function")
def client():
    """
    # Fixture yang akan dijalankan oleh Pytest sebelum setiap fungsi tes.
    """
    # # 1. Buat semua tabel di database testing sebelum tes dijalankan.
    Base.metadata.create_all(bind=engine)
    
    # # 2. 'yield' akan memberikan TestClient ke fungsi tes.
    # # Tes akan berjalan di sini.
    yield TestClient(app)
    
    # # 3. Setelah tes selesai, hapus semua tabel.
    # # Ini memastikan setiap tes dimulai dengan database yang bersih.
    Base.metadata.drop_all(bind=engine)

