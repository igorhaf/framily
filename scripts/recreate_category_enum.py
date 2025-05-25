import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def recreate_category_enum():
    db = SessionLocal()
    try:
        # Tenta criar o tipo ENUM se não existir
        db.execute(text("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'categoryenum') THEN
                    CREATE TYPE categoryenum AS ENUM ('FOOD', 'PERSONAL', 'HOUSEHOLD', 'OTHER');
                END IF;
            END$$;
        """))
        db.commit()
        print("ENUM categoryenum recriado (ou já existia) com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao recriar ENUM: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    recreate_category_enum() 