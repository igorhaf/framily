"""Update shopping categories

Revision ID: 20250521_1417
Revises: 20250521_1416
Create Date: 2025-05-21 14:17:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250521_1417'
down_revision = '20250521_1416'
branch_labels = None
depends_on = None

def upgrade():
    # Criar novo tipo de enum
    op.execute("CREATE TYPE category_enum_new AS ENUM ('FOOD', 'PERSONAL', 'HOUSEHOLD', 'OTHER')")
    
    # Converter valores existentes
    op.execute("""
        ALTER TABLE shopping_items 
        ALTER COLUMN category TYPE category_enum_new 
        USING CASE 
            WHEN category::text = 'CLEANING' THEN 'PERSONAL'::category_enum_new
            WHEN category::text = 'HYGIENE' THEN 'PERSONAL'::category_enum_new
            ELSE category::text::category_enum_new
        END
    """)
    
    # Remover tipo antigo e renomear novo
    op.execute('DROP TYPE category_enum')
    op.execute('ALTER TYPE category_enum_new RENAME TO category_enum')

def downgrade():
    # Criar tipo antigo
    op.execute("CREATE TYPE category_enum_old AS ENUM ('FOOD', 'CLEANING', 'HYGIENE', 'HOUSEHOLD', 'OTHER')")
    
    # Converter valores de volta
    op.execute("""
        ALTER TABLE shopping_items 
        ALTER COLUMN category TYPE category_enum_old 
        USING CASE 
            WHEN category::text = 'PERSONAL' THEN 'HYGIENE'::category_enum_old
            ELSE category::text::category_enum_old
        END
    """)
    
    # Remover tipo novo e renomear antigo
    op.execute('DROP TYPE category_enum')
    op.execute('ALTER TYPE category_enum_old RENAME TO category_enum') 