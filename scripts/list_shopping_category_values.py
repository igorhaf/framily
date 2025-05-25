import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def list_category_values():
    db = SessionLocal()
    try:
        print("Valores distintos em shopping_items.category:")
        result = db.execute(text("SELECT DISTINCT category FROM shopping_items"))
        for row in result:
            print(f"- {row[0]}")
        print("\nTipo da coluna:")
        result = db.execute(text("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'shopping_items' AND column_name = 'category'
        """))
        for row in result:
            print(f"- column_name: {row[0]}, data_type: {row[1]}, udt_name: {row[2]}")
    except Exception as e:
        print(f"Erro ao listar valores: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_category_values() 