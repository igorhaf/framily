"""update_enum_status

Revision ID: 805c269c35c5
Revises: d2b829e134e2
Create Date: 2025-05-20 01:29:38.082079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import String, Enum
from sqlalchemy.sql import table, column
from enum import Enum as PyEnum


# revision identifiers, used by Alembic.
revision: str = '805c269c35c5'
down_revision: Union[str, None] = 'd2b829e134e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Definição das enumerações antigas e novas
class OldStatusEnum(str, PyEnum):
    PENDING = "PENDING"
    PURCHASED = "BOUGHT"
    CANCELLED = "CANCELLED"

class NewStatusEnum(str, PyEnum):
    PENDING = "PENDING"
    BOUGHT = "BOUGHT"
    CANCELLED = "CANCELLED"


def upgrade() -> None:
    # Definir a tabela para fazer update
    shopping_items = table('shopping_items',
        column('id', sa.Integer),
        column('status', sa.String)
    )
    
    # Atualizar os valores: de PURCHASED para BOUGHT
    op.execute(
        shopping_items.update()
        .where(shopping_items.c.status == 'PURCHASED')
        .values(status='BOUGHT')
    )
    
    # Atualizando a definição da enum no SQLAlchemy
    with op.batch_alter_table('shopping_items') as batch_op:
        # Primeiro remove a antiga
        batch_op.alter_column('status', 
                    existing_type=Enum(OldStatusEnum),
                    type_=String,
                    nullable=False)
        
        # Depois adiciona a nova
        batch_op.alter_column('status',
                    existing_type=String,
                    type_=Enum(NewStatusEnum),
                    nullable=False)


def downgrade() -> None:
    # Definir a tabela para fazer downgrade
    shopping_items = table('shopping_items',
        column('id', sa.Integer),
        column('status', sa.String)
    )
    
    # Atualizar os valores: de BOUGHT para PURCHASED
    op.execute(
        shopping_items.update()
        .where(shopping_items.c.status == 'BOUGHT')
        .values(status='PURCHASED')
    )
    
    # Atualizando a definição da enum no SQLAlchemy
    with op.batch_alter_table('shopping_items') as batch_op:
        # Primeiro remove a nova
        batch_op.alter_column('status', 
                    existing_type=Enum(NewStatusEnum),
                    type_=String,
                    nullable=False)
        
        # Depois adiciona a antiga
        batch_op.alter_column('status',
                    existing_type=String,
                    type_=Enum(OldStatusEnum),
                    nullable=False)
