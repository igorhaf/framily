"""make family_id optional in tasks

Revision ID: b3cf2a5af36e
Revises: 805c269c35c5
Create Date: 2025-05-21 15:08:43.371444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3cf2a5af36e'
down_revision: Union[str, None] = '805c269c35c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
