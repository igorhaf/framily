import os
import sys
import logging

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backup_db import create_backup
from restore_db import restore_backup

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def backup_and_restore():
    try:
        # Fazer backup do estado atual
        logger.info("Fazendo backup do estado atual...")
        backup_file = create_backup()
        if not backup_file:
            logger.error("Falha ao criar backup")
            return False

        # Restaurar o backup
        logger.info("Restaurando backup...")
        if restore_backup(backup_file):
            logger.info("Processo de backup e restauração concluído com sucesso!")
            return True
        else:
            logger.error("Falha ao restaurar backup")
            return False

    except Exception as e:
        logger.error(f"Erro durante o processo de backup e restauração: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Se um arquivo de backup for especificado, apenas restaurar
        backup_file = sys.argv[1]
        restore_backup(backup_file)
    else:
        # Caso contrário, fazer backup e restaurar
        backup_and_restore() 