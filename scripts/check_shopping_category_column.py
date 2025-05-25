import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def check_category_column():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'shopping_items' AND column_name = 'category'
        """))
        print("Tipo da coluna 'category' em 'shopping_items':")
        for row in result:
            print(f"- column_name: {row[0]}, data_type: {row[1]}, udt_name: {row[2]}")
    except Exception as e:
        print(f"Erro ao consultar coluna: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_category_column() 