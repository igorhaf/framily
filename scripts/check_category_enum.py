import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def check_category_enum():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT unnest(enum_range(NULL::category_enum))
        """))
        print("Valores atuais do ENUM category_enum:")
        for row in result:
            print(f"- {row[0]}")
    except Exception as e:
        print(f"Erro ao consultar ENUM: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_category_enum() 