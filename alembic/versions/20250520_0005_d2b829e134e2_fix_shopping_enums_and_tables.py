"""Fix shopping enums and tables

Revision ID: d2b829e134e2
Revises: fa56e85af8e0
Create Date: 2025-05-20 00:05:44.818292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2b829e134e2'
down_revision: Union[str, None] = 'fa56e85af8e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar enum para categorias
    op.execute("CREATE TYPE category_enum AS ENUM ('market', 'home', 'personal', 'other')")
    
    # Criar enum para prioridades
    op.execute("CREATE TYPE priority_enum AS ENUM ('low', 'medium', 'high')")
    
    # Criar enum para status
    op.execute("CREATE TYPE status_enum AS ENUM ('pending', 'purchased', 'cancelled')")
    
    # Alterar colunas para usar os enums
    op.execute("ALTER TABLE shopping_items ALTER COLUMN category TYPE category_enum USING category::category_enum")
    op.execute("ALTER TABLE shopping_items ALTER COLUMN priority TYPE priority_enum USING priority::priority_enum")
    op.execute("ALTER TABLE shopping_items ALTER COLUMN status TYPE status_enum USING status::status_enum")


def downgrade() -> None:
    # Remover enums
    op.execute("DROP TYPE category_enum")
    op.execute("DROP TYPE priority_enum")
    op.execute("DROP TYPE status_enum")
