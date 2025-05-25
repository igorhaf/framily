import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def list_enum_types():
    db = SessionLocal()
    try:
        print("Tipos ENUM existentes no banco:")
        result = db.execute(text("""
            SELECT t.typname, e.enumlabel
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            ORDER BY t.typname, e.enumsortorder
        """))
        enums = {}
        for row in result:
            typname = row[0]
            label = row[1]
            if typname not in enums:
                enums[typname] = []
            enums[typname].append(label)
        for typname, labels in enums.items():
            print(f"- {typname}: {', '.join(labels)}")
    except Exception as e:
        print(f"Erro ao listar ENUMs: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_enum_types() 