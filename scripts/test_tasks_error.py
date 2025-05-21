import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao PYTHONPATH
root_dir = str(Path(__file__).parent.parent)
sys.path.append(root_dir)

import requests
import json
import traceback

def test_tasks_error():
    print("Iniciando testes de erro de tarefas...")
    print("Testando erro de carregamento de tarefas...")
    print("--------------------------------------------------")

    base_url = "http://localhost:8000/api/v1"
    params = {"skip": 0, "limit": 100}

    # Testando endpoint de tarefas
    print("Testando endpoint de tarefas...")
    try:
        response = requests.get(f"{base_url}/tasks/", params=params)
        if response.status_code == 200:
            print("✅ Sucesso nas tarefas!")
            print("Dados das tarefas:", json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Erro nas tarefas! Status: {response.status_code}")
            print("Resposta:", response.text)
    except Exception as e:
        print(f"❌ Erro ao testar tarefas: {str(e)}")
        print("Traceback:", traceback.format_exc())

if __name__ == "__main__":
    test_tasks_error() 