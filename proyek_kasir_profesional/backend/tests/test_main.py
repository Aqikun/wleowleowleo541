# Lokasi file: tests/test_main.py

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # # INI ADALAH BARIS YANG DIPERBAIKI
    assert response.json() == {"message": "Selamat datang di API Kasir Profesional v1.0.0"}