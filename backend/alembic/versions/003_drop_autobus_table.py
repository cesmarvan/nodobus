"""Drop autobus table

Revision ID: 003
Revises: 002
Create Date: 2026-04-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, Sequence[str], None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - drop autobus table and related indexes."""
    # Drop indexes first
    op.execute('DROP INDEX IF EXISTS idx_autobus_posicion')
    op.execute('DROP INDEX IF EXISTS ix_autobus_linea_id')
    op.execute('DROP INDEX IF EXISTS ix_autobus_vehiculo')
    op.execute('DROP INDEX IF EXISTS ix_autobus_id')
    # Drop foreign key constraint and table
    op.drop_table('autobus')


def downgrade() -> None:
    """Downgrade schema - recreate autobus table."""
    from geoalchemy2 import Geometry
    import sqlalchemy as sa
    
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
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_id ON autobus (id)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_vehiculo ON autobus (vehiculo)')
    op.execute('CREATE INDEX IF NOT EXISTS ix_autobus_linea_id ON autobus (linea_id)')
    op.execute('CREATE INDEX IF NOT EXISTS idx_autobus_posicion ON autobus USING GIST (posicion)')
