# nama file: src/main.py

# Mengimpor FastAPI dan router-router dari setiap domain
from fastapi import FastAPI
from src.domains.users import router as users_router
from src.domains.auth import router as auth_router
from src.domains.products import router as products_router
from src.domains.transactions import router as transactions_router
from src.domains.reports import router as reports_router
from src.domains.inventory import router as inventory_router
from src.domains.collaboration import router as collaboration_router

# Membuat instance utama aplikasi FastAPI
app = FastAPI(
    title="API Kasir Profesional",
    description="Backend untuk aplikasi kasir profesional dengan fitur lengkap.",
    version="1.0.0"
)

# Endpoint root untuk memeriksa apakah API berjalan
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "OK", "message": "Selamat datang di API Kasir Profesional!"}

# Mendaftarkan semua router ke aplikasi utama
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(transactions_router.router)
app.include_router(reports_router.router)
app.include_router(collaboration_router.router)

# PERBAIKAN FINAL: Hapus argumen 'prefix' dari sini karena sudah didefinisikan di dalam router.py
app.include_router(inventory_router.router)