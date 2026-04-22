"""Add autobus model

Revision ID: 002
Revises: 001
Create Date: 2026-04-22 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, Sequence[str], None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create autobus table
    op.create_table(
        'autobus',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vehiculo', sa.Integer(), nullable=False),
        sa.Column('posicion', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.Column('sentido', sa.Integer(), nullable=False),
        sa.Column('linea_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['linea_id'], ['linea.id']),
        sa.PrimaryKeyConstraint('id')
    )
    # Create indexes using raw SQL to avoid naming issues with geo columns
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_id ON autobus (id)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_vehiculo ON autobus (vehiculo)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_linea_id ON autobus (linea_id)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_autobus_posicion ON autobus USING GIST (posicion)')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop autobus table and indexes
    op.execute('DROP INDEX IF EXISTS idx_autobus_posicion')
    op.execute('DROP INDEX IF EXISTS ix_autobus_linea_id')
    op.execute('DROP INDEX IF EXISTS ix_autobus_vehiculo')
    op.execute('DROP INDEX IF EXISTS ix_autobus_id')
    op.drop_table('autobus')
