# Documentação da API - Family Dashboard

Esta pasta contém arquivos de coleção e ambiente do Postman para testar e explorar a API do Family Dashboard.

## Arquivos Incluídos

- `FastAPIProject_collection.json`: Coleção do Postman com todos os endpoints da API
- `FastAPIProject_environment.json`: Arquivo de ambiente do Postman para desenvolvimento local

## Como Importar no Postman

1. Abra o Postman
2. Clique em "Import" no canto superior esquerdo
3. Arraste os arquivos ou clique para selecionar os arquivos `FastAPIProject_collection.json` e `FastAPIProject_environment.json`
4. Confirme a importação

## Como Usar

1. No canto superior direito, selecione o ambiente "Family Dashboard API - Desenvolvimento" no dropdown
2. A variável `baseUrl` será automaticamente configurada para `http://localhost:8000`
3. Se sua aplicação estiver rodando em uma porta ou host diferente, você pode editar esta variável no ambiente

## Endpoints Disponíveis

A coleção está organizada em pastas por funcionalidade:

### Tarefas
- GET `/api/v1/tasks/`: Lista todas as tarefas
- POST `/api/v1/tasks/`: Cria uma nova tarefa

### Finanças
- GET `/api/v1/finance/categories/`: Lista todas as categorias financeiras
- GET `/api/v1/finance/transactions/`: Lista todas as transações
- GET `/api/v1/finance/budgets/`: Lista todos os orçamentos

### Saúde
- GET `/api/v1/health/appointments/`: Lista todas as consultas médicas
- POST `/api/v1/health/appointments/`: Cria uma nova consulta médica
- GET `/api/v1/health/medications/`: Lista todos os medicamentos
- POST `/api/v1/health/medications/`: Cria um novo medicamento
- GET `/api/v1/health/exams/`: Lista todos os exames
- POST `/api/v1/health/exams/`: Cria um novo exame

### Calendário
- GET `/api/v1/calendar/events/`: Lista eventos do calendário dentro de um período
- POST `/api/v1/calendar/events/`: Cria um novo evento no calendário
- PUT `/api/v1/calendar/events/{event_id}`: Atualiza um evento existente
- DELETE `/api/v1/calendar/events/{event_id}`: Remove um evento do calendário

## Parâmetros Comuns

Muitos endpoints aceitam os seguintes parâmetros:

- `skip`: Número de registros a pular (paginação)
- `limit`: Número máximo de registros a retornar
- `family_id` ou `family_member_id`: Filtra resultados por família ou membro da família

## Detalhes Sobre os Formatos

- Datas: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
- Cores do calendário: Código hexadecimal (ex: #4285F4)
- Tipos de evento: string (trabalho, aniversario, saude, escola, lazer, esporte) 