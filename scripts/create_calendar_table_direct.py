import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

# Criar engine de conexão
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# SQL para criar as tabelas necessárias
sql = '''
-- Criar tabela families se não existir
CREATE TABLE IF NOT EXISTS families (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR
);

-- Criar tabela family_members se não existir
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
'''

# Executar o SQL
try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print('✅ Tabelas criadas com sucesso!')
except Exception as e:
    print(f'❌ Erro ao criar tabelas: {e}')

# Verificar se a tabela foi criada
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'calendar_events')"))
        exists = result.scalar()
        
    if exists:
        print('✅ Tabela calendar_events existe no banco de dados!')
    else:
        print('❌ Tabela calendar_events NÃO existe no banco de dados!')
except Exception as e:
    print(f'❌ Erro ao verificar tabela: {e}') 