# alembic/helpers.py
from alembic import op
import sqlalchemy as sa


def create_enum(*values, name):
    e = sa.Enum(*values, name=name)
    e.create(op.get_bind(), checkfirst=True)
    return e


def drop_enum(name):
    sa.Enum(name=name).drop(op.get_bind(), checkfirst=True)
