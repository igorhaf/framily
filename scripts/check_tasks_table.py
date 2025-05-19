import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import sqlalchemy
from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks'"))
    columns = result.fetchall()
    column_names = [column[0] for column in columns]
    if "family_member_id" in column_names:
        print("A coluna family_member_id existe na tabela tasks.")
    else:
        print("A coluna family_member_id não existe na tabela tasks.")

    if 'family_member_id' in column_names:
        print('OK: family_member_id existe na tabela tasks.')
    else:
        print('ERRO: family_member_id NÃO existe na tabela tasks!')
        print('Colunas atuais:', column_names)
        print('Você deve dropar e recriar a tabela tasks ou o banco de dados.') 