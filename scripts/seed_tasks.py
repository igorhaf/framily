from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import crud_task
from app.schemas.task import TaskCreate

# Lista de títulos de exemplo para tasks
SAMPLE_TITLES = [
    "Fazer compras no supermercado",
    "Pagar contas mensais",
    "Levar as crianças ao médico",
    "Reunião da escola",
    "Limpeza geral da casa",
    "Manutenção do carro",
    "Preparar jantar em família",
    "Ajudar com a lição de casa",
    "Organizar documentos",
    "Fazer exercícios",
    "Marcar consulta dentista",
    "Comprar material escolar",
    "Consertar vazamento",
    "Lavar roupa",
    "Cortar grama",
    "Planejar férias em família",
    "Fazer backup dos documentos",
    "Atualizar calendário familiar",
    "Revisar orçamento mensal",
    "Organizar fotos da família"
]

# Lista de descrições de exemplo
SAMPLE_DESCRIPTIONS = [
    "Prioridade alta - precisa ser feito hoje",
    "Tarefa mensal recorrente",
    "Importante para a saúde da família",
    "Compromisso escolar importante",
    "Manutenção regular da casa",
    "Cuidados com o veículo da família",
    "Momento importante de união familiar",
    "Suporte educacional para as crianças",
    "Organização administrativa familiar",
    "Cuidados com a saúde e bem-estar",
    "Acompanhamento de saúde regular",
    "Preparação para o ano letivo",
    "Manutenção preventiva da casa",
    "Tarefas domésticas semanais",
    "Manutenção do jardim",
    "Planejamento de lazer familiar",
    "Segurança dos dados familiares",
    "Organização dos compromissos",
    "Controle financeiro familiar",
    "Preservação das memórias familiares"
]

def create_sample_tasks(db: Session, user_id: int, family_id: int) -> None:
    """Cria 20 tasks de exemplo no banco de dados."""
    now = datetime.utcnow()
    
    for i in range(20):
        # Gera uma data de vencimento aleatória entre hoje e 30 dias no futuro
        due_date = now + timedelta(days=random.randint(0, 30))
        
        # Cria a task
        task_in = TaskCreate(
            title=SAMPLE_TITLES[i],
            description=SAMPLE_DESCRIPTIONS[i],
            due_date=due_date,
            completed=random.choice([True, False]),
            user_id=user_id,
            family_id=family_id
        )
        crud_task.create(db=db, obj_in=task_in)

def main() -> None:
    """Função principal para executar o script de seed."""
    db = SessionLocal()
    try:
        # Aqui você deve substituir pelos IDs reais de um usuário e família existentes
        user_id = 1  # ID do usuário de exemplo
        family_id = 1  # ID da família de exemplo
        create_sample_tasks(db, user_id, family_id)
        print("✅ Dados de exemplo para tasks criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 