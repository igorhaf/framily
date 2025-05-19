"""create tasks table

Revision ID: create_tasks_table
Revises: 
Create Date: 2025-05-19 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'create_tasks_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('due_date', sa.DateTime(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('family_id', sa.Integer(), nullable=False),
        sa.Column('family_member_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['family_id'], ['families.id'], ),
        sa.ForeignKeyConstraint(['family_member_id'], ['family_members.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('tasks') 