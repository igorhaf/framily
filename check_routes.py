import requests
import sys
import os

def check_shopping_debug():
    try:
        # Verificar se o servidor está rodando
        response = requests.get("http://localhost:8000/shopping_debug")
        if response.status_code == 200:
            content = response.text
            print("Conteúdo da página shopping_debug:")
            # Vamos procurar por alguns padrões específicos
            if "Esta lista não possui itens!" in content:
                print("ERRO: Mensagem 'Esta lista não possui itens!' encontrada na página")
            else:
                print("A página não mostra a mensagem de erro 'Esta lista não possui itens!'")

            # Verificar se há itens sendo listados
            if "<tbody class=\"divide-y divide-gray-200 bg-white\">" in content:
                print("A tabela de itens existe na página")
                
                # Verificar se há linhas na tabela (itens)
                if "<tr>" in content:
                    print("Há linhas na tabela de itens")
                else:
                    print("ERRO: Não há linhas na tabela de itens")
        else:
            print(f"Erro ao acessar a página: {response.status_code}")
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")

if __name__ == "__main__":
    check_shopping_debug() 