import os
import sys
import random
from datetime import datetime, timedelta, date

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

# Criar engine de conexão
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

print("=== Iniciando população do banco de dados com dados iniciais ===")

# Limpar dados antigos para evitar duplicações
clean_sql = '''
-- Limpar dados existentes e reiniciar sequences
TRUNCATE TABLE finance_transactions RESTART IDENTITY CASCADE;
TRUNCATE TABLE finance_budgets RESTART IDENTITY CASCADE;
TRUNCATE TABLE finance_categories RESTART IDENTITY CASCADE;
TRUNCATE TABLE health_exams RESTART IDENTITY CASCADE;
TRUNCATE TABLE health_medications RESTART IDENTITY CASCADE;
TRUNCATE TABLE health_appointments RESTART IDENTITY CASCADE;
TRUNCATE TABLE calendar_events RESTART IDENTITY CASCADE;
TRUNCATE TABLE tasks RESTART IDENTITY CASCADE;
TRUNCATE TABLE family_members RESTART IDENTITY CASCADE;
TRUNCATE TABLE families RESTART IDENTITY CASCADE;
'''

# Criar família
family_sql = '''
-- Inserir família
INSERT INTO families (id, name, description)
VALUES (1, 'Família Silva', 'Família principal');
'''

# Criar membros da família
family_members_sql = '''
-- Inserir membros da família
INSERT INTO family_members (name, family_id, birth_date, gender) VALUES
('João Silva', 1, '1980-05-10', 'masculino'),
('Maria Silva', 1, '1985-03-15', 'feminino'),
('Pedro Silva', 1, '2010-11-20', 'masculino'),
('Ana Silva', 1, '2015-07-05', 'feminino');
'''

# Criar categorias financeiras
finance_categories_sql = '''
-- Inserir categorias de receita
INSERT INTO finance_categories (name, description, type, family_id) VALUES
('Salário', 'Salários e pagamentos regulares', 'INCOME', 1),
('Investimentos', 'Rendimentos de investimentos', 'INCOME', 1),
('Freelance', 'Trabalhos extras e freelance', 'INCOME', 1),
('Presentes', 'Dinheiro recebido de presente', 'INCOME', 1);

-- Inserir categorias de despesa
INSERT INTO finance_categories (name, description, type, family_id) VALUES
('Alimentação', 'Supermercado, restaurantes, delivery', 'EXPENSE', 1),
('Moradia', 'Aluguel, prestação, condomínio, IPTU', 'EXPENSE', 1),
('Transporte', 'Combustível, transporte público, manutenção', 'EXPENSE', 1),
('Saúde', 'Plano de saúde, medicamentos, consultas', 'EXPENSE', 1),
('Educação', 'Mensalidades, cursos, material escolar', 'EXPENSE', 1),
('Lazer', 'Cinema, shows, viagens', 'EXPENSE', 1),
('Vestuário', 'Roupas, calçados, acessórios', 'EXPENSE', 1),
('Serviços', 'Internet, telefone, streaming', 'EXPENSE', 1);
'''

# Criar transações financeiras
transactions_sql = '''
-- Inserir transações de receita para os últimos 3 meses
-- Mês atual
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(5000.00, 'Salário - João', CURRENT_DATE - INTERVAL '5 days', 'INCOME', 1, 1),
(3500.00, 'Salário - Maria', CURRENT_DATE - INTERVAL '5 days', 'INCOME', 1, 1),
(350.00, 'Dividendos', CURRENT_DATE - INTERVAL '10 days', 'INCOME', 2, 1);

-- Mês anterior
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(5000.00, 'Salário - João', CURRENT_DATE - INTERVAL '1 month 5 days', 'INCOME', 1, 1),
(3500.00, 'Salário - Maria', CURRENT_DATE - INTERVAL '1 month 5 days', 'INCOME', 1, 1),
(280.00, 'Dividendos', CURRENT_DATE - INTERVAL '1 month 10 days', 'INCOME', 2, 1),
(1200.00, 'Projeto freelance', CURRENT_DATE - INTERVAL '1 month 15 days', 'INCOME', 3, 1);

-- Mês retrasado
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(5000.00, 'Salário - João', CURRENT_DATE - INTERVAL '2 month 5 days', 'INCOME', 1, 1),
(3500.00, 'Salário - Maria', CURRENT_DATE - INTERVAL '2 month 5 days', 'INCOME', 1, 1),
(310.00, 'Dividendos', CURRENT_DATE - INTERVAL '2 month 10 days', 'INCOME', 2, 1);

-- Inserir transações de despesa para os últimos 3 meses
-- Mês atual
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(1500.00, 'Aluguel', CURRENT_DATE - INTERVAL '2 days', 'EXPENSE', 6, 1),
(950.00, 'Supermercado', CURRENT_DATE - INTERVAL '3 days', 'EXPENSE', 5, 1),
(380.00, 'Combustível', CURRENT_DATE - INTERVAL '4 days', 'EXPENSE', 7, 1),
(200.00, 'Farmácia', CURRENT_DATE - INTERVAL '6 days', 'EXPENSE', 8, 1),
(150.00, 'Internet', CURRENT_DATE - INTERVAL '8 days', 'EXPENSE', 12, 1),
(80.00, 'Streaming', CURRENT_DATE - INTERVAL '8 days', 'EXPENSE', 12, 1),
(350.00, 'Roupas', CURRENT_DATE - INTERVAL '10 days', 'EXPENSE', 11, 1),
(120.00, 'Restaurante', CURRENT_DATE - INTERVAL '12 days', 'EXPENSE', 5, 1);

-- Mês anterior
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(1500.00, 'Aluguel', CURRENT_DATE - INTERVAL '1 month 2 days', 'EXPENSE', 6, 1),
(920.00, 'Supermercado', CURRENT_DATE - INTERVAL '1 month 5 days', 'EXPENSE', 5, 1),
(400.00, 'Combustível', CURRENT_DATE - INTERVAL '1 month 8 days', 'EXPENSE', 7, 1),
(150.00, 'Farmácia', CURRENT_DATE - INTERVAL '1 month 10 days', 'EXPENSE', 8, 1),
(150.00, 'Internet', CURRENT_DATE - INTERVAL '1 month 12 days', 'EXPENSE', 12, 1),
(80.00, 'Streaming', CURRENT_DATE - INTERVAL '1 month 12 days', 'EXPENSE', 12, 1),
(500.00, 'Material escolar', CURRENT_DATE - INTERVAL '1 month 15 days', 'EXPENSE', 9, 1),
(180.00, 'Restaurante', CURRENT_DATE - INTERVAL '1 month 18 days', 'EXPENSE', 5, 1);

-- Mês retrasado
INSERT INTO finance_transactions (amount, description, date, type, category_id, family_id) VALUES
(1500.00, 'Aluguel', CURRENT_DATE - INTERVAL '2 month 2 days', 'EXPENSE', 6, 1),
(880.00, 'Supermercado', CURRENT_DATE - INTERVAL '2 month 5 days', 'EXPENSE', 5, 1),
(350.00, 'Combustível', CURRENT_DATE - INTERVAL '2 month 8 days', 'EXPENSE', 7, 1),
(180.00, 'Farmácia', CURRENT_DATE - INTERVAL '2 month 10 days', 'EXPENSE', 8, 1),
(150.00, 'Internet', CURRENT_DATE - INTERVAL '2 month 12 days', 'EXPENSE', 12, 1),
(80.00, 'Streaming', CURRENT_DATE - INTERVAL '2 month 12 days', 'EXPENSE', 12, 1),
(250.00, 'Cinema e lazer', CURRENT_DATE - INTERVAL '2 month 15 days', 'EXPENSE', 10, 1),
(150.00, 'Restaurante', CURRENT_DATE - INTERVAL '2 month 18 days', 'EXPENSE', 5, 1);
'''

# Criar orçamentos
budgets_sql = '''
-- Inserir orçamentos para o mês atual
INSERT INTO finance_budgets (amount, category_id, family_id, month, year) VALUES
(1000.00, 5, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(1500.00, 6, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(400.00, 7, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(300.00, 8, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(500.00, 9, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(300.00, 10, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(400.00, 11, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE)),
(250.00, 12, 1, EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE));
'''

# Criar tarefas
tasks_sql = '''
-- Inserir tarefas
INSERT INTO tasks (title, description, due_date, status, family_member_id) VALUES
('Compras no supermercado', 'Comprar itens para a semana', CURRENT_DATE + INTERVAL '2 days', 'pending', 1),
('Reunião na escola', 'Reunião com professores', CURRENT_DATE + INTERVAL '5 days', 'pending', 2),
('Lavar o carro', 'Levar o carro para lavar e encerar', CURRENT_DATE + INTERVAL '3 days', 'pending', 1),
('Pagar contas', 'Pagar contas de água e luz', CURRENT_DATE + INTERVAL '1 day', 'pending', 2),
('Consulta médica', 'Consulta de rotina com clínico geral', CURRENT_DATE + INTERVAL '10 days', 'pending', 3),
('Limpar o quarto', 'Organizar brinquedos e roupas', CURRENT_DATE, 'in_progress', 4),
('Fazer tarefa escolar', 'Projeto de ciências', CURRENT_DATE + INTERVAL '7 days', 'pending', 3),
('Comprar presente de aniversário', 'Aniversário da vovó', CURRENT_DATE + INTERVAL '15 days', 'pending', 2),
('Cortar grama', 'Cortar a grama do jardim', CURRENT_DATE - INTERVAL '2 days', 'completed', 1),
('Consertar prateleira', 'Prateleira do quarto das crianças', CURRENT_DATE - INTERVAL '5 days', 'completed', 1);
'''

# Criar eventos de calendário
calendar_events_sql = '''
-- Inserir eventos de calendário
INSERT INTO calendar_events (title, description, start_date, end_date, event_type, family_member_id, location, is_all_day, color) VALUES
('Reunião de trabalho', 'Reunião com equipe de desenvolvimento', CURRENT_DATE + INTERVAL '2 days 10 hours', CURRENT_DATE + INTERVAL '2 days 12 hours', 'trabalho', 1, 'Escritório', false, '#4285F4'),
('Aniversário de Pedro', 'Festa de aniversário', CURRENT_DATE + INTERVAL '10 days', CURRENT_DATE + INTERVAL '10 days', 'aniversario', 3, 'Casa', true, '#EA4335'),
('Consulta médica', 'Pediatra', CURRENT_DATE + INTERVAL '5 days 14 hours', CURRENT_DATE + INTERVAL '5 days 15 hours', 'saude', 4, 'Clínica Central', false, '#34A853'),
('Feira de ciências', 'Apresentação do projeto escolar', CURRENT_DATE + INTERVAL '7 days 9 hours', CURRENT_DATE + INTERVAL '7 days 17 hours', 'escola', 3, 'Escola Municipal', false, '#FBBC05'),
('Viagem em família', 'Viagem para a praia', CURRENT_DATE + INTERVAL '20 days', CURRENT_DATE + INTERVAL '25 days', 'lazer', NULL, 'Praia Grande', true, '#46BDC6'),
('Reunião de pais', 'Reunião sobre o desempenho escolar', CURRENT_DATE + INTERVAL '8 days 18 hours 30 minutes', CURRENT_DATE + INTERVAL '8 days 20 hours', 'escola', 2, 'Escola Municipal', false, '#FBBC05'),
('Treino de futebol', 'Treino semanal', CURRENT_DATE + INTERVAL '3 days 16 hours', CURRENT_DATE + INTERVAL '3 days 18 hours', 'esporte', 3, 'Campo Municipal', false, '#0F9D58'),
('Dia de compras', 'Compras mensais no shopping', CURRENT_DATE + INTERVAL '15 days 14 hours', CURRENT_DATE + INTERVAL '15 days 20 hours', 'lazer', 2, 'Shopping Center', false, '#7B2CBF');
'''

# Criar registros de saúde (consultas, medicamentos, exames)
health_appointments_sql = '''
-- Inserir consultas médicas
INSERT INTO health_appointments (title, description, date, time, type, doctor, specialty, location, notes, status, family_member_id) VALUES
('Consulta pediátrica', 'Consulta de rotina', CURRENT_DATE + INTERVAL '10 days', '14:00', 'consulta', 'Dr. Roberto Pereira', 'Pediatria', 'Centro Médico', NULL, 'agendado', 3),
('Consulta pediátrica', 'Consulta de rotina', CURRENT_DATE + INTERVAL '10 days', '15:00', 'consulta', 'Dr. Roberto Pereira', 'Pediatria', 'Centro Médico', NULL, 'agendado', 4),
('Oftalmologista', 'Verificação anual', CURRENT_DATE + INTERVAL '15 days', '10:00', 'consulta', 'Dra. Ana Luz', 'Oftalmologia', 'Clínica Visão', NULL, 'agendado', 1),
('Dentista', 'Limpeza semestral', CURRENT_DATE + INTERVAL '5 days', '09:00', 'consulta', 'Dr. Carlos Souza', 'Odontologia', 'Consultório Odontológico', NULL, 'agendado', 2),
('Cardiologista', 'Checkup anual', CURRENT_DATE + INTERVAL '20 days', '11:00', 'consulta', 'Dr. Marcos Coração', 'Cardiologia', 'Hospital Central', NULL, 'agendado', 1);
'''

health_medications_sql = '''
-- Inserir medicamentos
INSERT INTO health_medications (name, dosage, frequency, start_date, end_date, family_member_id) VALUES
('Vitamina C', '500mg', 'Uma vez ao dia', CURRENT_DATE - INTERVAL '10 days', CURRENT_DATE + INTERVAL '20 days', 3),
('Amoxicilina', '250mg', 'A cada 8 horas', CURRENT_DATE - INTERVAL '5 days', CURRENT_DATE + INTERVAL '2 days', 4),
('Anti-alérgico', '10mg', 'Uma vez ao dia', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE + INTERVAL '15 days', 1),
('Ibuprofeno', '200mg', 'A cada 8 horas, se necessário', CURRENT_DATE, NULL, 2);
'''

health_exams_sql = '''
-- Inserir exames
INSERT INTO health_exams (name, description, date, result, family_member_id) VALUES
('Hemograma completo', 'Exame de sangue de rotina', CURRENT_DATE - INTERVAL '20 days', 'Dentro dos parâmetros normais', 1),
('Hemograma completo', 'Exame de sangue de rotina', CURRENT_DATE - INTERVAL '20 days', 'Dentro dos parâmetros normais', 2),
('Raio-X de tórax', 'Avaliação pulmonar', CURRENT_DATE - INTERVAL '10 days', 'Normal', 4),
('Exame de vista', 'Avaliação da acuidade visual', CURRENT_DATE - INTERVAL '2 months', 'Necessita de óculos para leitura', 1),
('Exame de urina', 'Urina tipo I', CURRENT_DATE - INTERVAL '15 days', 'Normal', 3);
'''

# Executar os scripts SQL
try:
    with engine.connect() as conn:
        print("1. Limpando dados existentes...")
        conn.execute(text(clean_sql))
        print("   ✅ Dados limpos com sucesso!")
        
        print("2. Inserindo família...")
        conn.execute(text(family_sql))
        print("   ✅ Família criada!")
        
        print("3. Inserindo membros da família...")
        conn.execute(text(family_members_sql))
        print("   ✅ Membros da família criados!")
        
        print("4. Inserindo categorias financeiras...")
        conn.execute(text(finance_categories_sql))
        print("   ✅ Categorias financeiras criadas!")
        
        print("5. Inserindo transações financeiras...")
        conn.execute(text(transactions_sql))
        print("   ✅ Transações financeiras criadas!")
        
        print("6. Inserindo orçamentos...")
        conn.execute(text(budgets_sql))
        print("   ✅ Orçamentos criados!")
        
        print("7. Inserindo tarefas...")
        conn.execute(text(tasks_sql))
        print("   ✅ Tarefas criadas!")
        
        print("8. Inserindo eventos de calendário...")
        conn.execute(text(calendar_events_sql))
        print("   ✅ Eventos de calendário criados!")
        
        print("9. Inserindo consultas médicas...")
        conn.execute(text(health_appointments_sql))
        print("   ✅ Consultas médicas criadas!")
        
        print("10. Inserindo medicamentos...")
        conn.execute(text(health_medications_sql))
        print("   ✅ Medicamentos criados!")
        
        print("11. Inserindo exames...")
        conn.execute(text(health_exams_sql))
        print("   ✅ Exames criados!")
        
        conn.commit()
        print("\n✅ Todos os dados foram inseridos com sucesso!")
except Exception as e:
    print(f"\n❌ Erro durante a inserção de dados: {e}")
    sys.exit(1)

print("\n=== População de dados concluída. O sistema está pronto para uso! ===") 