import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

# Criar engine de conexão
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# SQL para criar todas as tabelas necessárias
sql = '''
-- Criar tabela families
CREATE TABLE IF NOT EXISTS families (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR
);

-- Criar tabela family_members
CREATE TABLE IF NOT EXISTS family_members (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    family_id INTEGER REFERENCES families(id),
    birth_date DATE,
    gender VARCHAR
);

-- Criar tabela calendar_events
CREATE TABLE IF NOT EXISTS calendar_events (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    event_type VARCHAR NOT NULL,
    family_member_id INTEGER REFERENCES family_members(id),
    location VARCHAR,
    is_all_day BOOLEAN NOT NULL DEFAULT FALSE,
    color VARCHAR
);

-- Criar tabela finance_categories
CREATE TABLE IF NOT EXISTS finance_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    type VARCHAR NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL
);

-- Criar tabela finance_transactions
CREATE TABLE IF NOT EXISTS finance_transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    description VARCHAR,
    date TIMESTAMP NOT NULL,
    type VARCHAR NOT NULL,
    category_id INTEGER REFERENCES finance_categories(id) NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL
);

-- Criar tabela finance_budgets
CREATE TABLE IF NOT EXISTS finance_budgets (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    category_id INTEGER REFERENCES finance_categories(id) NOT NULL,
    family_id INTEGER REFERENCES families(id) NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL
);

-- Criar tabela tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    due_date TIMESTAMP,
    status VARCHAR NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    family_id INTEGER REFERENCES families(id),
    family_member_id INTEGER REFERENCES family_members(id)
);

-- Criar tabela health_appointments
CREATE TABLE IF NOT EXISTS health_appointments (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    date TIMESTAMP NOT NULL,
    time VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    doctor VARCHAR,
    specialty VARCHAR,
    location VARCHAR,
    notes TEXT,
    status VARCHAR NOT NULL DEFAULT 'agendado',
    family_member_id INTEGER REFERENCES family_members(id) NOT NULL
);

-- Criar tabela health_medications
CREATE TABLE IF NOT EXISTS health_medications (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    dosage VARCHAR,
    frequency VARCHAR,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    status VARCHAR NOT NULL DEFAULT 'ativo',
    notes TEXT,
    family_member_id INTEGER REFERENCES family_members(id) NOT NULL
);

-- Criar tabela health_exams
CREATE TABLE IF NOT EXISTS health_exams (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    date TIMESTAMP NOT NULL,
    location VARCHAR,
    doctor VARCHAR,
    notes TEXT,
    result VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'agendado',
    family_member_id INTEGER REFERENCES family_members(id) NOT NULL
);
'''

# Executar o SQL
try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print('Tabelas criadas com sucesso!')
except Exception as e:
    print(f'❌ Erro ao criar tabelas: {e}')

# Verificar tabelas existentes
try:
    insp = inspect(engine)
    tables = insp.get_table_names()
    
    print(f"\nTabelas encontradas no banco de dados:")
    for table in sorted(tables):
        print(f"  - {table}")
    
    # Verificar tabelas específicas
    required_tables = [
        'families', 
        'family_members', 
        'calendar_events', 
        'finance_categories', 
        'finance_transactions', 
        'finance_budgets',
        'tasks',
        'health_appointments',
        'health_medications',
        'health_exams'
    ]
    
    missing_tables = [table for table in required_tables if table not in tables]
    
    if missing_tables:
        print(f"\nTabelas ausentes: {', '.join(missing_tables)}")
    else:
        print("\nTodas as tabelas necessárias existem no banco de dados!")
        
except Exception as e:
    print(f"\nErro ao verificar tabelas: {e}")

print("\n=== Processo concluído. Reinicie o servidor FastAPI (uvicorn main:app --reload) ===") 