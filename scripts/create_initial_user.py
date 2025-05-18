from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.family import Family
from datetime import datetime

def create_initial_data(db: Session) -> tuple[int, int]:
    """Cria usuário e família inicial e retorna seus IDs."""
    # Criar família
    family = Family(
        name="Família Exemplo",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(family)
    db.flush()  # Para obter o ID da família

    # Criar usuário
    user = User(
        email="user@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGRH3nw.3Ji",  # senha: password123
        full_name="Usuário Exemplo",
        is_active=True,
        is_superuser=True,
        family_id=family.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(family)
    
    return user.id, family.id

def main() -> None:
    """Função principal para criar dados iniciais."""
    db = SessionLocal()
    try:
        user_id, family_id = create_initial_data(db)
        print(f"✅ Usuário (ID: {user_id}) e Família (ID: {family_id}) criados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main() 