import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def fix_category_enum_definitive():
    db = SessionLocal()
    try:
        print("Alterando coluna 'category' para TEXT...")
        db.execute(text("ALTER TABLE shopping_items ALTER COLUMN category TYPE TEXT;"))
        db.commit()
        print("Coluna alterada para TEXT.")

        print("Removendo ENUM antigo 'categoryenum'...")
        try:
            db.execute(text("DROP TYPE categoryenum;"))
            db.commit()
            print("ENUM antigo removido.")
        except Exception as e:
            print(f"Aviso: não foi possível remover ENUM antigo: {e}")
            db.rollback()

        print("Criando ENUM novo 'categoryenum'...")
        db.execute(text("""
            CREATE TYPE categoryenum AS ENUM ('FOOD', 'PERSONAL', 'HOUSEHOLD', 'OTHER');
        """))
        db.commit()
        print("ENUM novo criado.")

        print("Corrigindo valores inválidos para 'PERSONAL'...")
        db.execute(text("""
            UPDATE shopping_items SET category = 'PERSONAL' WHERE category NOT IN ('FOOD', 'PERSONAL', 'HOUSEHOLD', 'OTHER');
        """))
        db.commit()
        print("Valores corrigidos.")

        print("Convertendo coluna 'category' para ENUM 'categoryenum'...")
        db.execute(text("""
            ALTER TABLE shopping_items ALTER COLUMN category TYPE categoryenum USING category::categoryenum;
        """))
        db.commit()
        print("Coluna convertida para ENUM com sucesso!")

        print("Valores finais na coluna:")
        result = db.execute(text("SELECT DISTINCT category FROM shopping_items"))
        for row in result:
            print(f"- {row[0]}")
    except Exception as e:
        db.rollback()
        print(f"Erro durante a correção definitiva: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_category_enum_definitive() 