from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
import importlib
import pkgutil
from pathlib import Path
import sys

# Add project root to path so imports work
sys.path.insert(0, str(Path(__file__).parents[1]))

from app.core.database import Base
from app.core.config import settings

# Auto-import all models
models_path = Path(__file__).parents[1] / "app" / "models"
for _, module_name, _ in pkgutil.iter_modules([str(models_path)]):
    importlib.import_module(f"app.models.{module_name}")

target_metadata = Base.metadata

# this is the Alembic Config object
config = context.config

fileConfig(config.config_file_name)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    # Use settings if available, fall back to alembic.ini
    url = (
        settings.database_url if settings else config.get_main_option("sqlalchemy.url")
    )
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        settings.database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
