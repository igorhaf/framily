import subprocess
import sys
from pathlib import Path

def run_migrations():
    """Executa as migrações do Alembic."""
    print("🔄 Executando migrações...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Migrações executadas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def seed_database():
    """Executa os scripts de seed do banco de dados."""
    print("🌱 Populando banco de dados...")
    try:
        # Importa e executa o script de seed de tasks
        from seed_tasks import main as seed_tasks
        seed_tasks()
        print("✅ Tasks criadas com sucesso!")

        # Importa e executa o script de seed de shopping
        from seed_shopping_data import main as seed_shopping
        seed_shopping()
        print("✅ Listas de compras criadas com sucesso!")

        print("✅ Banco de dados populado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao popular banco de dados: {e}")
        return False

def main():
    """Função principal para inicializar e popular o banco de dados."""
    # Adiciona o diretório raiz ao PYTHONPATH
    root_dir = Path(__file__).parent.parent
    sys.path.append(str(root_dir))

    # Executa as migrações
    if not run_migrations():
        sys.exit(1)

    # Popula o banco de dados
    if not seed_database():
        sys.exit(1)

    print("✨ Banco de dados inicializado e populado com sucesso!")

if __name__ == "__main__":
    main() 