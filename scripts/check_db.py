import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

print("Verificando conexão com o banco de dados...")
print(f"URL do banco de dados: {settings.SQLALCHEMY_DATABASE_URI}")

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    # Listar todas as tabelas
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
    tables = result.fetchall()
    print("\nTabelas existentes:")
    for table in tables:
        print(f"- {table[0]}")
        
        # Listar colunas de cada tabela
        result = conn.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table[0]}'"))
        columns = result.fetchall()
        print("  Colunas:")
        for column in columns:
            print(f"  - {column[0]}")
        print() 