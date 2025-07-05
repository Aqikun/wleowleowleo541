# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. Impor CORSMiddleware
from .core.database import engine
from .models import user_model, product_model, transaction_model, inventory_model
from .api.v1 import api_router

# Membuat semua tabel di database jika belum ada
user_model.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
transaction_model.Base.metadata.create_all(bind=engine)
inventory_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyek Kasir Profesional API",
    description="API untuk aplikasi kasir profesional dengan fitur kolaborasi realtime.",
    version="1.0.0"
)

# 2. Tambahkan middleware CORS di sini
origins = [
    "http://localhost",
    "http://localhost:8080",
    # Tambahkan port tempat Flutter Web Anda berjalan jika berbeda atau spesifik
    # Contoh: "http://localhost:56490" (port bisa berubah-ubah saat development)
    "http://localhost:9100",  # Untuk Flutter DevTools
    "http://127.0.0.1",
]

# Cara terbaik untuk development adalah mengizinkan semua origin dengan wildcard,
# tapi untuk produksi, sebaiknya daftar originnya spesifik.
# Untuk development, Anda bisa menyederhanakannya menjadi:
# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Mengizinkan origin yang didefinisikan di atas
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)

# Menyertakan router API utama
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint root untuk memeriksa apakah API berjalan.
    """
    return {"message": "Selamat datang di API Kasir Profesional!"}