import sys
import os
from pathlib import Path
from sqlalchemy import text

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from app.db.session import SessionLocal

def check_db_schema():
    db = SessionLocal()
    try:
        # Verificar colunas da tabela shopping_items
        result = db.execute(text("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'shopping_items'
        """))
        
        print("\nShopping Items Columns:")
        for row in result:
            print(f"{row[0]}: {row[1]} ({row[2]})")
        
        # Verificar colunas da tabela shopping_lists
        result = db.execute(text("""
            SELECT column_name, data_type, udt_name 
            FROM information_schema.columns 
            WHERE table_name = 'shopping_lists'
        """))
        
        print("\nShopping Lists Columns:")
        for row in result:
            print(f"{row[0]}: {row[1]} ({row[2]})")
        
        # Verificar tipos enum
        result = db.execute(text("""
            SELECT t.typname, e.enumlabel
            FROM pg_type t
            JOIN pg_enum e ON t.oid = e.enumtypid
            ORDER BY t.typname, e.enumsortorder
        """))
        
        enums = {}
        for row in result:
            enum_type = row[0]
            enum_value = row[1]
            if enum_type not in enums:
                enums[enum_type] = []
            enums[enum_type].append(enum_value)
        
        print("\nEnum Types:")
        for enum_type, values in enums.items():
            print(f"{enum_type}: {', '.join(values)}")
        
    except Exception as e:
        print(f"Erro ao verificar esquema do banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_db_schema() 