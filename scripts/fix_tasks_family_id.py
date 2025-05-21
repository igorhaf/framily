from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_tasks_family_id():
    # Criar engine
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    with engine.connect() as conn:
        # Primeiro, vamos verificar se existe uma família
        result = conn.execute(text("SELECT id FROM families LIMIT 1"))
        family = result.fetchone()
        
        if not family:
            print("Nenhuma família encontrada. Criando uma família padrão...")
            conn.execute(text("""
                INSERT INTO families (name, description)
                VALUES ('Família Silva', 'Família principal')
            """))
            conn.commit()
            
            # Buscar o ID da família recém-criada
            result = conn.execute(text("SELECT id FROM families LIMIT 1"))
            family = result.fetchone()
        
        family_id = family[0]
        print(f"Usando família ID: {family_id}")
        
        # Atualizar todas as tarefas sem family_id
        conn.execute(text("""
            UPDATE tasks
            SET family_id = :family_id
            WHERE family_id IS NULL
        """), {"family_id": family_id})
        
        conn.commit()
        
        # Verificar resultado
        result = conn.execute(text("SELECT COUNT(*) FROM tasks WHERE family_id IS NULL"))
        null_count = result.scalar()
        print(f"\nTarefas sem family_id após a correção: {null_count}")

if __name__ == "__main__":
    fix_tasks_family_id() 