import os
import sys
import subprocess
from datetime import datetime
import logging
import time

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nome do container do PostgreSQL
POSTGRES_CONTAINER = "family_dashboard_db"

def create_backup():
    try:
        # Criar diretório de backup se não existir
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logger.info(f"Diretório de backup criado: {backup_dir}")

        # Nome do arquivo de backup com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"family_dashboard_backup_{timestamp}.sql")

        # Comando para fazer o backup usando Docker
        cmd = [
            "docker",
            "exec",
            POSTGRES_CONTAINER,
            "pg_dump",
            "-h", settings.POSTGRES_SERVER,
            "-U", settings.POSTGRES_USER,
            "-d", settings.POSTGRES_DB,
            "-F", "c",  # Formato customizado (comprimido)
            "-f", f"/tmp/backup.sql"
        ]

        # Executar o comando de backup com timeout
        logger.info("Iniciando backup do banco de dados...")
        process = subprocess.Popen(
            cmd,
            env=dict(os.environ, PGPASSWORD=settings.POSTGRES_PASSWORD)
        )

        # Aguardar o processo com timeout
        try:
            process.wait(timeout=30)  # 30 segundos de timeout
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("Timeout ao criar backup")
            return None

        if process.returncode == 0:
            # Copiar o arquivo de backup do container para o host
            copy_cmd = [
                "docker",
                "cp",
                f"{POSTGRES_CONTAINER}:/tmp/backup.sql",
                backup_file
            ]
            process = subprocess.Popen(copy_cmd)
            process.wait(timeout=10)  # 10 segundos de timeout

            if process.returncode == 0:
                logger.info(f"Backup criado com sucesso: {backup_file}")
                return backup_file
            else:
                logger.error("Erro ao copiar arquivo de backup do container")
                return None
        else:
            logger.error("Erro ao criar backup")
            return None

    except Exception as e:
        logger.error(f"Erro ao criar backup: {str(e)}")
        return None

if __name__ == "__main__":
    create_backup() 