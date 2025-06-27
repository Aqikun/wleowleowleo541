# backend/src/main.py

# # Mengimpor FastAPI dan router-router dari setiap domain
from fastapi import FastAPI
from src.core.database import engine, Base
from src.domains.users import router as users_router
from src.domains.auth import router as auth_router
from src.domains.products import router as products_router
from src.domains.transactions import router as transactions_router
from src.domains.reports import router as reports_router
from src.domains.inventory import router as inventory_router
from src.domains.collaboration import router as collaboration_router

# # Membuat instance utama aplikasi FastAPI
app = FastAPI(
    title="API Kasir Profesional",
    description="Backend untuk aplikasi kasir profesional dengan fitur lengkap.",
    version="1.0.0"
)

# # Endpoint root untuk memeriksa apakah API berjalan
@app.get("/", tags=["Root"])
def read_root():
    # # PERBAIKAN 2: Pastikan respons ini sama persis dengan yang ada di tes.
    return {"status": "OK", "message": "Selamat datang di API Kasir Profesional!"}

# # Mendaftarkan semua router ke aplikasi utama
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(transactions_router.router)
app.include_router(reports_router.router)
app.include_router(collaboration_router.router)

# # PERBAIKAN 1: Daftarkan inventory_router dengan prefix yang benar.
# # Ini akan membuat semua endpoint di dalamnya diawali dengan /inventory.
# # Contoh: /suppliers/ akan menjadi /inventory/suppliers/
app.include_router(inventory_router.router, prefix="/inventory", tags=["Inventory"])