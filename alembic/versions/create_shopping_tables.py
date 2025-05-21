"""create shopping tables

Revision ID: create_shopping_tables
Revises: 
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'create_shopping_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Criar enum types
    op.execute("CREATE TYPE category_enum AS ENUM ('FOOD', 'CLEANING', 'HYGIENE', 'HOUSEHOLD', 'OTHER')")
    op.execute("CREATE TYPE priority_enum AS ENUM ('LOW', 'MEDIUM', 'HIGH')")
    op.execute("CREATE TYPE status_enum AS ENUM ('PENDING', 'BOUGHT', 'CANCELLED')")

    # Criar tabela de listas de compras
    op.create_table(
        'shopping_lists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de itens de compras
    op.create_table(
        'shopping_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=True),
        sa.Column('category', postgresql.ENUM('FOOD', 'CLEANING', 'HYGIENE', 'HOUSEHOLD', 'OTHER', name='category_enum'), nullable=True),
        sa.Column('priority', postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', name='priority_enum'), nullable=True),
        sa.Column('status', postgresql.ENUM('PENDING', 'BOUGHT', 'CANCELLED', name='status_enum'), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('shopping_list_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['shopping_list_id'], ['shopping_lists.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('shopping_items')
    op.drop_table('shopping_lists')
    op.execute('DROP TYPE status_enum')
    op.execute('DROP TYPE priority_enum')
    op.execute('DROP TYPE category_enum') 