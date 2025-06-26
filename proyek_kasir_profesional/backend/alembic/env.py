# alembic/env.py
import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# # Menambahkan path 'src' ke dalam path sistem agar kita bisa mengimpor dari src
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# # Impor dari proyek kita
from core.database import Base
from core.config import settings

# # Impor semua model Anda di sini agar Base.metadata mengetahuinya
from domains.users import models as user_models
from domains.products import models as product_models
from domains.transactions import models as transaction_models
from domains.inventory import models as inventory_models # <-- TAMBAHKAN INI

# # Ini adalah konfigurasi Alembic, dihasilkan dari file alembic.ini
config = context.config

# # Menginterpretasikan file config untuk logging Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# # Menetapkan metadata dari Base kita ke 'target_metadata'
target_metadata = Base.metadata

# # Menambahkan variabel DATABASE_URL dari settings kita ke dalam config Alembic
config.set_main_option('DATABASE_URL', settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
