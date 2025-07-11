"""add foreign key to post table

Revision ID: e542b3877b55
Revises: 3b87e001b897
Create Date: 2025-06-28 14:11:18.555065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e542b3877b55'
down_revision: Union[str, Sequence[str], None] = '3b87e001b897'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column("owner_id", sa.Integer(), nullable = False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
