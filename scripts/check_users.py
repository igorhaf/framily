from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import traceback

try:
    print('Usuários cadastrados:')
    db = SessionLocal()
    users = db.query(User).all()
    for u in users:
        print(f"ID: {u.id} | Nome: {u.name} | Email: {u.email} | Tipo: {u.type}")

    def ensure_admin():
        admin = db.query(User).filter_by(email="admin@admin.com").first()
        if not admin:
            admin = User(
                name="Administrador",
                email="admin@admin.com",
                password_hash=get_password_hash("admin"),
                type="client"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Usuário admin criado com sucesso!")
        else:
            print("Usuário admin@admin.com já existe.")

    ensure_admin()
    db.close()
except Exception as e:
    print("Erro ao acessar/criar usuários:")
    traceback.print_exc() 