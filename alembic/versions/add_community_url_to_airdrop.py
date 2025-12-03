"""add community_url to airdrop

Revision ID: add_community_url
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_community_url'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add community_url column to airdrops table
    op.add_column('airdrops', sa.Column('community_url', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove community_url column from airdrops table
    op.drop_column('airdrops', 'community_url')

