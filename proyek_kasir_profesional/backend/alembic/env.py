# nama file: alembic/env.py

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Mengimpor Base dari file database.py
from src.core.database import Base, engine # <-- Impor engine dari database

# Mengimpor semua model Anda di sini agar terdeteksi oleh autogenerate
from src.domains.users.models import User
from src.domains.products.models import Product
from src.domains.transactions.models import Transaction, TransactionDetail
from src.domains.inventory.models import Supplier, PurchaseOrder, PurchaseOrderDetail, StockOpname, StockOpnameDetail
from src.domains.collaboration.models import ChatMessage

# ini adalah objek Konfigurasi Alembic, yang menyediakan
# akses ke nilai-nilai dalam file .ini yang sedang digunakan.
config = context.config

# Menginterpretasikan file konfigurasi untuk logging Python.
# Baris ini pada dasarnya mengatur logger.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# tambahkan objek MetaData model Anda di sini
# untuk dukungan 'autogenerate'
# dari myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# nilai-nilai lain dari konfigurasi, yang ditentukan oleh kebutuhan env.py,
# dapat diperoleh di sini:
# my_important_option = config.get_main_option("my_important_option")
# ... dll.


def run_migrations_offline() -> None:
    """Menjalankan migrasi dalam mode 'offline'.

    Ini mengkonfigurasi konteks hanya dengan URL
    dan bukan Engine, meskipun Engine juga dapat diterima
    di sini. Dengan melewati Engine, kita bahkan tidak memerlukan
    DBAPI untuk tersedia.

    Panggilan ke context.execute() akan menulis DDL yang diberikan ke output skrip.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Aktifkan batch mode untuk dukungan SQLite
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Menjalankan migrasi dalam mode 'online'.

    Dalam skenario ini kita perlu membuat Engine
    dan mengaitkan koneksi dengan konteks.

    """
    # Gunakan engine yang sudah diimpor dari core.database
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # Aktifkan batch mode untuk dukungan SQLite
            render_as_batch=True 
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()