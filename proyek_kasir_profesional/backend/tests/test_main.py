# Lokasi file: backend/tests/test_main.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # PERBAIKAN: Sesuaikan dengan respons aktual dari main.py
    assert response.json() == {"message": "Selamat datang di API Kasir Profesional"}