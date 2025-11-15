from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from dotenv import load_dotenv

# ----------------------------------------------------------------------
# 1. SETUP PROJECT PATH & ENVIRONMENT VARIABLES
# ----------------------------------------------------------------------
# Menambahkan folder project saat ini ke path python agar bisa import 'app'
sys.path.append(os.getcwd())

# Memuat variabel dari file .env
load_dotenv()

# Mengambil URL Database dari .env
database_url = os.getenv("DATABASE_URL")

# ----------------------------------------------------------------------
# 2. CONFIGURATION
# ----------------------------------------------------------------------
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# TIMPA url di alembic.ini dengan URL asli dari .env
# Ini penting supaya password tidak perlu ditulis di alembic.ini
config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----------------------------------------------------------------------
# 3. LOAD MODELS (METADATA)
# ----------------------------------------------------------------------
# Import Base dan Model-model kamu di sini
from app.core.database import Base
# Kita import model spesifik supaya SQLAlchemy "sadar" kalau tabel ini ada
from app.models.models import User, Journal, MoodLog 

# Set target metadata agar Alembic bisa mendeteksi perubahan tabel
target_metadata = Base.metadata

# ----------------------------------------------------------------------
# 4. MIGRATION FUNCTIONS (OFFLINE & ONLINE)
# ----------------------------------------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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