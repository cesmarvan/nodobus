"""Initial migration

Revision ID: 23c92576e242
Revises: 
Create Date: 2026-04-22 11:57:23.678038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create parada table
    op.create_table(
        'parada',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nodo', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('localizacion', Geometry(geometry_type='POINT', srid=4326), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parada_nodo'), 'parada', ['nodo'], unique=False)
    op.create_index(op.f('ix_parada_id'), 'parada', ['id'], unique=False)

    # Create linea table
    op.create_table(
        'linea',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=False),
        sa.Column('destino', sa.String(length=255), nullable=False),
        sa.Column('labelLinea', sa.String(length=50), nullable=False),
        sa.Column('linea', sa.Integer(), nullable=False),
        sa.Column('nombreLinea', sa.String(length=255), nullable=False),
        sa.Column('recorrido', Geometry(geometry_type='LINESTRING', srid=4326), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_linea_linea'), 'linea', ['linea'], unique=False)
    op.create_index(op.f('ix_linea_id'), 'linea', ['id'], unique=False)

    # Create parada_linea table
    op.create_table(
        'parada_linea',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('parada_id', sa.Integer(), nullable=False),
        sa.Column('linea_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['parada_id'], ['parada.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['linea_id'], ['linea.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_parada_linea_parada_id'), 'parada_linea', ['parada_id'], unique=False)
    op.create_index(op.f('ix_parada_linea_id'), 'parada_linea', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop parada_linea table
    op.drop_index(op.f('ix_parada_linea_id'), table_name='parada_linea')
    op.drop_index(op.f('ix_parada_linea_parada_id'), table_name='parada_linea')
    op.drop_table('parada_linea')

    # Drop linea table
    op.drop_index(op.f('ix_linea_id'), table_name='linea')
    op.drop_index(op.f('ix_linea_linea'), table_name='linea')
    op.drop_table('linea')

    # Drop parada table
    op.drop_index(op.f('ix_parada_id'), table_name='parada')
    op.drop_index(op.f('ix_parada_nodo'), table_name='parada')
    op.drop_table('parada')

