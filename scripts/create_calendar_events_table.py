import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

sql = '''
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

try:
    with engine.connect() as conn:
        conn.execute(text(sql))
        print('Tabela calendar_events criada com sucesso!')
except Exception as e:
    print(f'Erro ao criar tabela: {e}') 