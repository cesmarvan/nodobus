"""creacion tabla incidencias

Revision ID: 003
Revises: 002
Create Date: 2026-04-23 08:00:54.968918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, Sequence[str], None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'incidencia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(), nullable=False),
        sa.Column('descripcion', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('parada_id', sa.Integer(), nullable=True),
        sa.Column('linea_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['parada_id'], ['parada.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['linea_id'], ['linea.id'], ondelete='CASCADE'),
    )
    op.execute('CREATE INDEX IF NOT EXISTS ix_incidencia_id ON incidencia (id)')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute('DROP INDEX IF EXISTS ix_incidencia_id')
    op.drop_table('incidencia')
    # ### end Alembic commands ###
