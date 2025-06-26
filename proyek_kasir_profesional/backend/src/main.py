# backend/src/main.py
from fastapi import FastAPI

# Mengimpor router dari setiap domain
from src.domains.users import router as users_router
from src.domains.auth import router as auth_router
from src.domains.products import router as products_router
from src.domains.transactions import router as transactions_router
from src.domains.reports import router as reports_router
from src.domains.inventory import router as inventory_router # <-- BARU

app = FastAPI(
    title="API Kasir Profesional",
    description="Cetak biru API untuk sistem kasir yang skalabel dan modern.",
    version="0.1.0",
)

# Mendaftarkan setiap router ke aplikasi utama
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(transactions_router.router)
app.include_router(reports_router.router)
# # Menambahkan .router untuk menunjuk ke objek APIRouter yang benar
app.include_router(inventory_router.router, prefix="/inventory") # <-- DIPERBAIKI

@app.get("/", tags=["Root"])
def read_root():
    """
    # Endpoint root untuk memeriksa apakah API berjalan dengan baik.
    """
    return {"status": "OK", "message": "Selamat datang di API Kasir Profesional!"}
