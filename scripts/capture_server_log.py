import subprocess
import sys
import os

# Garantir que o diretório logs existe
os.makedirs("logs", exist_ok=True)

# Comando para iniciar o servidor e redirecionar a saída para um arquivo de log
cmd = ["uvicorn", "main:app", "--log-level", "debug", ">", "logs/server.log", "2>&1"]

# Executar o comando
print("Iniciando o servidor e capturando logs em logs/server.log...")
subprocess.run(" ".join(cmd), shell=True) 