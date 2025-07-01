# Lokasi file: src/main.py
# # PERBAIKAN: Menghapus baris "from src.main import app" yang menyebabkan circular import.

from fastapi import FastAPI

# # Impor router dari masing-masing file yang sudah kita pisahkan. Ini sudah benar.
from src.domains.users.auth_router import auth_router
from src.domains.users.users_router import users_router
from src.domains.products.router import router as products_router
from src.domains.transactions.router import router as transactions_router
from src.domains.inventory.router import router as inventory_router

app = FastAPI(
    title="API Kasir Profesional",
    description="Backend API untuk aplikasi kasir profesional dengan fitur lengkap.",
    version="1.0.0"
)

# # Daftarkan setiap router ke aplikasi utama. Ini juga sudah benar.
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(transactions_router)
app.include_router(inventory_router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Selamat datang di API Kasir Profesional v1.0.0"}