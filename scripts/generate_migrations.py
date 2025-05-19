import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao Python path
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

from alembic.config import Config
from alembic import command

def generate_migrations():
    # Configurar o Alembic
    alembic_cfg = Config("alembic.ini")
    
    # Gerar a migração
    command.revision(alembic_cfg, message="add_health_tables", autogenerate=True)
    
    print("Migrações geradas com sucesso!")

if __name__ == "__main__":
    generate_migrations() 