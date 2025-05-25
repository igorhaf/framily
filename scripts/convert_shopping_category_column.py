import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def convert_category_column():
    db = SessionLocal()
    try:
        db.execute(text("""
            ALTER TABLE shopping_items
            ALTER COLUMN category TYPE categoryenum
            USING category::text::categoryenum;
        """))
        db.commit()
        print("Coluna 'category' convertida para o tipo ENUM 'categoryenum' com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao converter coluna: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    convert_category_column() 