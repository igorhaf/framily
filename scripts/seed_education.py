import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.education import *
from app.db.session import SessionLocal
from datetime import datetime, date, timedelta

# Dados de exemplo
institutions_data = [
    {"nome": "Universidade Federal do Exemplo", "tipo": TipoInstituicaoEnum.FACULDADE, "descricao": "Faculdade pública de referência."},
    {"nome": "Colégio Exemplar", "tipo": TipoInstituicaoEnum.ESCOLA, "descricao": "Ensino fundamental e médio."},
    {"nome": "Plataforma Cursos Online", "tipo": TipoInstituicaoEnum.CURSO_ONLINE, "descricao": "Cursos de tecnologia e idiomas."},
    {"nome": "Workshop de Criatividade", "tipo": TipoInstituicaoEnum.WORKSHOP, "descricao": "Evento anual de inovação."},
]

events_data = [
    {"titulo": "Aula de Matemática", "descricao": "Geometria Analítica.", "data_hora": datetime.now() + timedelta(days=1), "tipo": TipoEventoEnum.AULA, "instituicao_idx": 1},
    {"titulo": "Prova de História", "descricao": "Conteúdo: Idade Média.", "data_hora": datetime.now() + timedelta(days=3), "tipo": TipoEventoEnum.PROVA, "instituicao_idx": 1},
    {"titulo": "Palestra sobre IA", "descricao": "Inteligência Artificial na Educação.", "data_hora": datetime.now() + timedelta(days=5), "tipo": TipoEventoEnum.PALESTRA, "instituicao_idx": 0},
    {"titulo": "Workshop de Design", "descricao": "Ferramentas digitais.", "data_hora": datetime.now() + timedelta(days=10), "tipo": TipoEventoEnum.OUTRO, "instituicao_idx": 3},
]

expenses_data = [
    {"descricao": "Mensalidade Universidade", "valor": 1200.00, "data": date.today() - timedelta(days=10), "categoria": CategoriaDespesaEnum.MENSALIDADE, "observacoes": "Referente a junho."},
    {"descricao": "Compra de livros didáticos", "valor": 350.50, "data": date.today() - timedelta(days=20), "categoria": CategoriaDespesaEnum.LIVRO, "observacoes": "Livros para o semestre."},
    {"descricao": "Material escolar", "valor": 180.00, "data": date.today() - timedelta(days=5), "categoria": CategoriaDespesaEnum.MATERIAL, "observacoes": "Cadernos, canetas, etc."},
    {"descricao": "Inscrição em curso online", "valor": 299.90, "data": date.today() - timedelta(days=2), "categoria": CategoriaDespesaEnum.OUTRO, "observacoes": "Curso de Python."},
]

def seed_education():
    db = SessionLocal()
    try:
        # Instituições
        institutions = []
        for data in institutions_data:
            inst = EducationInstitution(**data)
            db.add(inst)
            institutions.append(inst)
        db.flush()

        # Eventos
        for data in events_data:
            data_cp = data.copy()
            idx = data_cp.pop("instituicao_idx")
            data_cp["instituicao_id"] = institutions[idx].id
            event = EducationEvent(**data_cp)
            db.add(event)

        # Despesas
        for data in expenses_data:
            expense = EducationExpense(**data)
            db.add(expense)

        db.commit()
        print("Tabelas de educação populadas com sucesso!")
    except Exception as e:
        db.rollback()
        print(f"Erro ao popular tabelas de educação: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_education() 