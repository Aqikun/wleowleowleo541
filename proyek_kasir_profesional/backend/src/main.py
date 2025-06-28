# Lokasi file: src/main.py
# PERBAIKAN: Mendaftarkan router baru untuk otentikasi dan manajemen pengguna

from fastapi import FastAPI
# PERBAIKAN: Impor router spesifik yang sudah kita buat dari users.router
from src.domains.users.router import auth_router, users_router

# Impor router lain yang sudah ada
from src.domains.products import router as products_router
from src.domains.transactions import router as transactions_router
from src.domains.reports import router as reports_router
from src.domains.inventory import router as inventory_router
# Tambahkan impor untuk router kolaborasi jika belum ada
from src.domains.collaboration import router as collaboration_router

app = FastAPI(
    title="Aplikasi Kasir Profesional API",
    description="Dokumentasi API untuk Aplikasi Kasir Profesional.",
    version="1.0.0"
)

# --- Mendaftarkan Router ---
# Daftarkan router untuk otentikasi (login, forgot password, etc.)
app.include_router(auth_router)
# Daftarkan router untuk manajemen user (/users)
app.include_router(users_router)

# Daftarkan router-router lain dari setiap domain
app.include_router(products_router.router)
app.include_router(transactions_router.router)
app.include_router(reports_router.router)
app.include_router(inventory_router.router)
app.include_router(collaboration_router.router)


@app.get("/")
def read_root():
    return {"message": "Selamat datang di API Kasir Profesional"}