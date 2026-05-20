from logging.config import fileConfig
from sqlalchemy import create_engine, CheckConstraint, pool
from alembic import context
from alembic.autogenerate import comparators, renderers
from alembic.operations import ops
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


# --- Check constraint autogenerate support ---


@comparators.dispatch_for("table")
def compare_check_constraints(
    autogen_context, modify_table_ops, schema, tname, conn_table, metadata_table
):
    if metadata_table is None:
        return

    metadata_checks = {
        c.name: c
        for c in metadata_table.constraints
        if isinstance(c, CheckConstraint) and c.name
    }

    db_checks = (
        {
            c.name: c
            for c in conn_table.constraints
            if isinstance(c, CheckConstraint) and c.name
        }
        if conn_table is not None
        else {}
    )

    for name, constraint in metadata_checks.items():
        if name not in db_checks:
            modify_table_ops.ops.append(
                ops.CreateCheckConstraintOp(
                    name, tname, constraint.sqltext, schema=schema
                )
            )

    for name in db_checks:
        if name not in metadata_checks:
            modify_table_ops.ops.append(
                ops.DropConstraintOp(name, tname, schema=schema)
            )


@renderers.dispatch_for(ops.CreateCheckConstraintOp, replace=True)
def render_create_check_constraint(autogen_context, op):
    return (
        "op.create_check_constraint(\n"
        f"        {op.constraint_name!r},\n"
        f"        {op.table_name!r},\n"
        f"        {str(op.condition)!r},\n"
        + (f"        schema={op.schema!r},\n" if op.schema else "")
        + "    )"
    )


def include_object(object, name, type_, reflected, compare_to):
    return True


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = (
        settings.database_url if settings else config.get_main_option("sqlalchemy.url")
    )
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
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
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
