import sqlalchemy
from sqlalchemy import create_engine, text
from datetime import datetime

# Configuração do banco de dados
DATABASE_URL = "postgresql://postgres:postgres@localhost/family_dashboard"

print("Adicionando registros de teste na tabela 'tasks'...")
print(f"URL do banco de dados: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    # Inserir alguns registros de teste
    conn.execute(text("""
        INSERT INTO tasks (title, description, due_date, completed, created_at, updated_at, family_id, family_member_id)
        VALUES 
        ('Tarefa 1', 'Descrição da Tarefa 1', '2025-06-01 10:00:00', FALSE, :created_at, :updated_at, 1, 1),
        ('Tarefa 2', 'Descrição da Tarefa 2', '2025-06-02 10:00:00', FALSE, :created_at, :updated_at, 1, 1)
    """), {"created_at": datetime.utcnow(), "updated_at": datetime.utcnow()})
    conn.commit()
print("Registros de teste adicionados com sucesso!") 