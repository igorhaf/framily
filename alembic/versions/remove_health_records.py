"""remove health_records table

Revision ID: remove_health_records
Revises: 
Create Date: 2025-05-19 17:00:00.000000

"""
from alembic import op

revision = 'remove_health_records'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute('DROP TABLE IF EXISTS health_records CASCADE')

def downgrade():
    pass 