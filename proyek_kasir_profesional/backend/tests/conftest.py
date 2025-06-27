# backend/tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base, get_db
from src.core.config import settings
from src.main import app

# # Pastikan kita menggunakan database untuk TESTING
SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    # # Fixture ini berjalan otomatis untuk SETIAP tes karena 'autouse=True'.
    # # 1. Membuat semua tabel sebelum setiap tes.
    Base.metadata.create_all(bind=engine)
    # # 2. 'yield' menyerahkan kontrol ke fungsi tes.
    yield
    # # 3. Menghapus semua tabel setelah setiap tes.
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    # # Fixture ini sekarang hanya fokus menyediakan TestClient.
    # # Pengaturan database sudah di-handle oleh 'setup_database'.
    yield TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    # # Fixture ini hanya fokus menyediakan sesi dan transaksi.
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# # Alias untuk mendukung tes-tes lama yang mencari 'test_db_session'.
test_db_session = db_session