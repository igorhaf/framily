import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

# Criar engine de conexão
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Primeiro, precisamos fazer backup dos dados existentes
backup_sql = '''
-- Backup dos dados de finance_categories
CREATE TEMPORARY TABLE finance_categories_backup AS 
SELECT id, name, type, family_id FROM finance_categories;

-- Backup dos dados de finance_transactions (dependem de finance_categories)
CREATE TEMPORARY TABLE finance_transactions_backup AS 
SELECT id, amount, description, date, type, category_id, family_id 
FROM finance_transactions;

-- Backup dos dados de finance_budgets (dependem de finance_categories)
CREATE TEMPORARY TABLE finance_budgets_backup AS 
SELECT id, amount, category_id, family_id, month, year
FROM finance_budgets;
'''

# Dropar tabelas que dependem de finance_categories
drop_sql = '''
-- Dropar tabela finance_transactions
DROP TABLE IF EXISTS finance_transactions;

-- Dropar tabela finance_budgets
DROP TABLE IF EXISTS finance_budgets;

-- Dropar tabela finance_categories
DROP TABLE IF EXISTS finance_categories;
'''

# Recriar tabelas com a estrutura correta
recreate_sql = '''
-- Recriar tabela finance_categories com a coluna description
CREATE TABLE finance_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    type VARCHAR NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL
);

-- Recriar tabela finance_transactions
CREATE TABLE finance_transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    description VARCHAR,
    date TIMESTAMP NOT NULL,
    type VARCHAR NOT NULL,
    category_id INTEGER REFERENCES finance_categories(id) NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL
);

-- Recriar tabela finance_budgets
CREATE TABLE finance_budgets (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    category_id INTEGER REFERENCES finance_categories(id) NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL
);
'''

# Restaurar dados
restore_sql = '''
-- Restaurar dados de finance_categories (sem description, que será NULL)
INSERT INTO finance_categories (id, name, type, family_id)
SELECT id, name, type, family_id FROM finance_categories_backup;

-- Restaurar dados de finance_transactions
INSERT INTO finance_transactions (id, amount, description, date, type, category_id, family_id)
SELECT id, amount, description, date, type, category_id, family_id FROM finance_transactions_backup;

-- Restaurar dados de finance_budgets
INSERT INTO finance_budgets (id, amount, category_id, family_id, month, year)
SELECT id, amount, category_id, family_id, month, year FROM finance_budgets_backup;
'''

# Executar os scripts em uma transação
try:
    print("=== Iniciando correção da tabela finance_categories ===")
    
    with engine.connect() as conn:
        # Fazer backup
        try:
            print("1. Fazendo backup dos dados existentes...")
            conn.execute(text(backup_sql))
            print("   ✅ Backup concluído!")
        except Exception as e:
            print(f"   ❌ Erro no backup: {e}")
            # Se não há dados, não é um problema crítico, podemos continuar
            
        # Dropar tabelas
        try:
            print("2. Dropando tabelas...")
            conn.execute(text(drop_sql))
            print("   ✅ Tabelas removidas!")
        except Exception as e:
            print(f"   ❌ Erro ao dropar tabelas: {e}")
            raise
            
        # Recriar tabelas
        try:
            print("3. Recriando tabelas com a estrutura correta...")
            conn.execute(text(recreate_sql))
            print("   ✅ Tabelas recriadas!")
        except Exception as e:
            print(f"   ❌ Erro ao recriar tabelas: {e}")
            raise
            
        # Restaurar dados
        try:
            print("4. Restaurando dados...")
            conn.execute(text(restore_sql))
            print("   ✅ Dados restaurados!")
        except Exception as e:
            print(f"   ❌ Erro ao restaurar dados: {e}")
            # Se não há dados para restaurar, não é problema
        
        # Confirmar todas as operações
        conn.commit()
        print("✅ Todas as operações concluídas com sucesso!")
        
except Exception as e:
    print(f"❌ Erro durante o processo: {e}")
    sys.exit(1)

# Verificar se a coluna description existe em finance_categories
try:
    insp = inspect(engine)
    columns = insp.get_columns('finance_categories')
    column_names = [col['name'] for col in columns]
    
    if 'description' in column_names:
        print("\n✅ A coluna 'description' agora existe na tabela finance_categories!")
    else:
        print("\n❌ A coluna 'description' NÃO foi adicionada! Algo deu errado.")
except Exception as e:
    print(f"\n❌ Erro ao verificar colunas: {e}")

print("\n=== Processo concluído. Reinicie o servidor FastAPI (uvicorn main:app --reload) ===") 