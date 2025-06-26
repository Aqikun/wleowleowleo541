# backend/tests/test_main.py
from fastapi.testclient import TestClient
from src.main import app

# # Membuat klien tes khusus untuk aplikasi FastAPI kita.
# # Ini memungkinkan kita mengirim permintaan ke API tanpa perlu menjalankan server sungguhan.
client = TestClient(app)

# # Pytest akan secara otomatis menemukan fungsi yang namanya diawali dengan 'test_'.
def test_read_root():
    # # Mengirim permintaan GET ke endpoint root ("/") menggunakan klien tes.
    response = client.get("/")
    
    # # 'assert' adalah cara kita memeriksa apakah hasilnya sesuai harapan.
    # # Jika kondisi 'assert' tidak terpenuhi, tes akan gagal.
    
    # # 1. Memeriksa apakah status kode respons adalah 200 (yang berarti "OK").
    assert response.status_code == 200
    
    # # 2. Memeriksa apakah isi (body) respons dalam format JSON sesuai dengan yang kita harapkan.
    assert response.json() == {
        "status": "OK",
        "message": "Selamat datang di API Kasir Profesional!"
    }
