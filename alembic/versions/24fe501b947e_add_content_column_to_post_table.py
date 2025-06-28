"""add content column to post table

Revision ID: 24fe501b947e
Revises: d856216ad307
Create Date: 2025-06-28 13:57:25.659488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24fe501b947e'
down_revision: Union[str, Sequence[str], None] = 'd856216ad307'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", 'content')
    pass
