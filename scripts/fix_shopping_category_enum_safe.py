import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def fix_shopping_category_enum_safe():
    db = SessionLocal()
    try:
        print("Alterando coluna 'category' para TEXT...")
        db.execute(text("""
            ALTER TABLE shopping_items ALTER COLUMN category TYPE TEXT;
        """))
        db.commit()
        print("Coluna alterada para TEXT.")

        print("Corrigindo valores inválidos para 'PERSONAL'...")
        db.execute(text("""
            UPDATE shopping_items SET category = 'PERSONAL' WHERE category IN ('CLEANING', 'HYGIENE');
        """))
        db.commit()
        print("Valores corrigidos.")

        print("Convertendo coluna 'category' de volta para ENUM 'categoryenum'...")
        db.execute(text("""
            ALTER TABLE shopping_items ALTER COLUMN category TYPE categoryenum USING category::categoryenum;
        """))
        db.commit()
        print("Coluna convertida para ENUM com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro durante a correção segura: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_shopping_category_enum_safe() 