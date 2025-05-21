import os
import sys
import subprocess
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

def restore_backup(backup_file):
    try:
        if not os.path.exists(backup_file):
            logger.error(f"Arquivo de backup não encontrado: {backup_file}")
            return False

        # Copiar o arquivo de backup para o container
        temp_backup = "/tmp/restore.sql"
        copy_cmd = [
            "docker",
            "cp",
            backup_file,
            f"{POSTGRES_CONTAINER}:{temp_backup}"
        ]
        process = subprocess.Popen(copy_cmd)
        try:
            process.wait(timeout=10)  # 10 segundos de timeout
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("Timeout ao copiar arquivo de backup")
            return False

        if process.returncode != 0:
            logger.error("Erro ao copiar arquivo de backup para o container")
            return False

        # Comando para restaurar o backup
        cmd = [
            "docker",
            "exec",
            POSTGRES_CONTAINER,
            "pg_restore",
            "-h", settings.POSTGRES_SERVER,
            "-U", settings.POSTGRES_USER,
            "-d", settings.POSTGRES_DB,
            "-c",  # Limpar (drop) objetos antes de criar
            "-v",  # Modo verbose
            temp_backup
        ]

        # Executar o comando com timeout
        logger.info("Iniciando restauração do banco de dados...")
        process = subprocess.Popen(
            cmd,
            env=dict(os.environ, PGPASSWORD=settings.POSTGRES_PASSWORD)
        )

        try:
            process.wait(timeout=60)  # 60 segundos de timeout
        except subprocess.TimeoutExpired:
            process.kill()
            logger.error("Timeout ao restaurar banco de dados")
            return False

        if process.returncode == 0:
            logger.info("Banco de dados restaurado com sucesso!")
            return True
        else:
            logger.error("Erro ao restaurar banco de dados")
            return False

    except Exception as e:
        logger.error(f"Erro ao restaurar banco de dados: {str(e)}")
        return False

def get_latest_backup():
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        logger.error("Diretório de backup não encontrado")
        return None

    # Listar todos os arquivos de backup
    backup_files = [f for f in os.listdir(backup_dir) if f.startswith("family_dashboard_backup_")]
    if not backup_files:
        logger.error("Nenhum arquivo de backup encontrado")
        return None

    # Ordenar por data (mais recente primeiro)
    backup_files.sort(reverse=True)
    return os.path.join(backup_dir, backup_files[0])

if __name__ == "__main__":
    # Se nenhum arquivo for especificado, usar o mais recente
    if len(sys.argv) > 1:
        backup_file = sys.argv[1]
    else:
        backup_file = get_latest_backup()
        if not backup_file:
            logger.error("Nenhum arquivo de backup especificado ou encontrado")
            sys.exit(1)

    restore_backup(backup_file) 