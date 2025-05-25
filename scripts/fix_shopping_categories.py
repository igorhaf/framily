import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def fix_shopping_categories():
    db = SessionLocal()
    try:
        # Verificar quantos registros precisam ser corrigidos
        result = db.execute(text("""
            SELECT COUNT(*) FROM shopping_items WHERE category IN ('CLEANING', 'HYGIENE')
        """))
        count = result.scalar()
        print(f"Itens a corrigir: {count}")
        if count == 0:
            print("Nenhum item com categoria antiga encontrado.")
            return

        # Corrigir as categorias
        db.execute(text("""
            UPDATE shopping_items SET category = 'PERSONAL' WHERE category IN ('CLEANING', 'HYGIENE')
        """))
        db.commit()
        print(f"Corrigidos {count} itens para categoria 'PERSONAL'.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao corrigir categorias: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_shopping_categories() 