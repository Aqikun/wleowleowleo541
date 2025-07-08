# backend/src/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import engine, Base

# ===== Impor router dari setiap domain secara eksplisit =====
from src.domains.users.auth_router import auth_router
from src.domains.users.users_router import users_router
from src.domains.products.router import router as products_router
from src.domains.transactions.router import router as transactions_router
from src.domains.inventory.router import router as inventory_router
from src.domains.reports.router import router as reports_router
from src.domains.collaboration.router import router as collaboration_router
# Tambahkan router lain jika ada
# from src.domains.customers.router import router as customers_router
# from src.domains.branches.router import router as branches_router
# from src.domains.subscriptions.router import router as subscriptions_router
# ==========================================================

# Impor semua model agar tabelnya bisa dibuat
from src.domains.users import models as user_model
from src.domains.products import models as product_model
from src.domains.transactions import models as transaction_model
from src.domains.inventory import models as inventory_model
from src.domains.collaboration import models as collaboration_model
from src.domains.branches import models as branch_model
from src.domains.customers import models as customer_model
from src.domains.subscriptions import models as subscription_model

# Membuat semua tabel dari semua model yang diimpor
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Proyek Kasir Profesional API",
    description="API untuk aplikasi kasir profesional dengan fitur kolaborasi realtime.",
    version="1.0.0"
)

# Mengizinkan semua origin untuk development
origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Daftarkan semua router di sini =====
API_PREFIX = "/api/v1" 

app.include_router(auth_router, prefix=API_PREFIX, tags=["Authentication"])
app.include_router(users_router, prefix=API_PREFIX, tags=["Users"])
app.include_router(products_router, prefix=API_PREFIX, tags=["Products"])
app.include_router(transactions_router, prefix=API_PREFIX, tags=["Transactions"])
app.include_router(inventory_router, prefix=API_PREFIX, tags=["Inventory"])
app.include_router(reports_router, prefix=API_PREFIX, tags=["Reports"])
app.include_router(collaboration_router, prefix=API_PREFIX, tags=["Collaboration"])
# Daftarkan router lain di sini jika ada
# ==========================================


@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint root untuk memeriksa apakah API berjalan.
    """
    return {"message": "Selamat datang di API Kasir Profesional!"}