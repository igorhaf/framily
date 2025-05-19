"""initial

Revision ID: 4a11eb8f0d57
Revises: 39c10d608233
Create Date: 2025-05-19 15:54:37.778964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a11eb8f0d57'
down_revision: Union[str, None] = '39c10d608233'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
