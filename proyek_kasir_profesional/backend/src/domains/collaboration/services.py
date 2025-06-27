# backend/src/domains/collaboration/services.py

# # Mengimpor komponen yang diperlukan dari FastAPI dan Python
from fastapi import WebSocket
from collections import defaultdict
import json

# # Kelas ini akan mengelola semua koneksi WebSocket yang aktif.
class ConnectionManager:
    # # Konstruktor kelas.
    def __init__(self):
        # # self.active_connections adalah sebuah dictionary.
        # # Kunci (key) adalah 'room_name' (nama ruang obrolan).
        # # Nilai (value) adalah sebuah list yang berisi objek koneksi WebSocket.
        # # defaultdict(list) adalah trik agar kita tidak perlu memeriksa apakah sebuah room sudah ada sebelum menambahkan koneksi.
        self.active_connections: dict[str, list[WebSocket]] = defaultdict(list)

    # # Fungsi untuk menangani koneksi baru.
    async def connect(self, websocket: WebSocket, room_name: str):
        # # Menerima koneksi WebSocket.
        await websocket.accept()
        # # Menambahkan koneksi baru ke dalam daftar untuk ruangan yang ditentukan.
        self.active_connections[room_name].append(websocket)

    # # Fungsi untuk menangani saat pengguna terputus.
    def disconnect(self, websocket: WebSocket, room_name: str):
        # # Menghapus koneksi dari daftar untuk ruangan yang ditentukan.
        self.active_connections[room_name].remove(websocket)

    # # Fungsi untuk mengirim pesan ke semua koneksi di sebuah ruangan.
    async def broadcast(self, message: str, room_name: str):
        # # Loop melalui setiap koneksi yang aktif di dalam ruangan.
        for connection in self.active_connections[room_name]:
            # # Kirim pesan sebagai teks ke setiap koneksi.
            await connection.send_text(message)

# # Membuat satu instance dari ConnectionManager yang akan digunakan oleh seluruh aplikasi.
# # Ini memastikan semua pengguna berbagi "operator telepon" yang sama.
manager = ConnectionManager()