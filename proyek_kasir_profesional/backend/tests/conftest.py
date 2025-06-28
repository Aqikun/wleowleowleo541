# Lokasi file: tests/conftest.py
# PERBAIKAN TUNTAS: Menambahkan kembali fixture 'db_session'

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base, get_db
from src.core.config import settings
from src.main import app
from src.core.dependencies import get_current_user
from src.domains.users.models import User
from src.domains.users.schemas import UserRole

SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return User(id=1, username="testadmin", email="testadmin@example.com", role=UserRole.Admin, hashed_password="hashed")

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    yield TestClient(app)

# PERBAIKAN KUNCI: Menambahkan kembali fixture db_session yang hilang
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        transaction.rollback() # Selalu rollback untuk isolasi tes
        connection.close()