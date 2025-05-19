import os
import sys
import subprocess
import time

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

print("=== Iniciando limpeza e recriação do banco de dados ===")

# 1. Conectar ao banco
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
print("Conectado ao banco de dados PostgreSQL")

# 2. Limpar o banco executando o script SQL
with open('scripts/reset_db.sql', 'r') as sql_file:
    sql_script = sql_file.read()

try:
    with engine.connect() as conn:
        # Executar como transação única
        conn.execute(text(sql_script))
        conn.commit()
    print("Banco de dados limpo com sucesso!")
except Exception as e:
    print(f"Erro ao limpar o banco: {e}")
    sys.exit(1)

# 3. Criar todas as tabelas necessárias executando o script create_all_tables.py
try:
    print("Executando script de criação de tabelas...")
    result = subprocess.run(['python', 'scripts/create_all_tables.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erro ao executar create_all_tables.py: {result.stderr}")
        sys.exit(1)
    else:
        print("Tabelas criadas com sucesso!")
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")
    sys.exit(1)

# 4. Verificar se a tabela calendar_events foi criada
try:
    print("Verificando tabelas existentes...")
    time.sleep(2)  # Pequena pausa para garantir que tudo foi commitado
    
    with engine.connect() as conn:
        insp = inspect(engine)
        tables = insp.get_table_names()
        
    print(f"Tabelas encontradas: {tables}")
    
    if 'calendar_events' in tables:
        print(f"Tabela calendar_events criada com sucesso!")
    else:
        print("Tabela calendar_events NÃO encontrada!")
        sys.exit(1)
except Exception as e:
    print(f"Erro ao verificar tabelas: {e}")
    sys.exit(1)

print("\n=== Processo concluído com sucesso! ===")
print("Agora reinicie o servidor FastAPI (uvicorn main:app --reload)") 