"""initial

Revision ID: 92dbde45a3ff
Revises: 
Create Date: 2025-05-19 18:19:55.842135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92dbde45a3ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela de usuários
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Criar tabela de famílias
    op.create_table(
        'families',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de membros da família
    op.create_table(
        'family_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de eventos do calendário
    op.create_table(
        'calendar_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('family_member_id', sa.Integer(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('is_all_day', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('color', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de tarefas
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('family_member_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de categorias financeiras
    op.create_table(
        'finance_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de transações financeiras
    op.create_table(
        'finance_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['finance_categories.id'], ),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de orçamentos
    op.create_table(
        'finance_budgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['finance_categories.id'], ),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de consultas médicas
    op.create_table(
        'health_appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('doctor', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('family_member_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de medicamentos
    op.create_table(
        'health_medications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dosage', sa.String(), nullable=True),
        sa.Column('frequency', sa.String(), nullable=True),
        sa.Column('start_date', sa.DateTime(), nullable=False),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('family_member_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Criar tabela de exames
    op.create_table(
        'health_exams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('result', sa.String(), nullable=True),
        sa.Column('family_member_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('health_exams')
    op.drop_table('health_medications')
    op.drop_table('health_appointments')
    op.drop_table('finance_budgets')
    op.drop_table('finance_transactions')
    op.drop_table('finance_categories')
    op.drop_table('tasks')
    op.drop_table('calendar_events')
    op.drop_table('family_members')
    op.drop_table('families')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
