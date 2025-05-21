from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base
import enum

class TipoInstituicaoEnum(str, enum.Enum):
    FACULDADE = "Faculdade"
    ESCOLA = "Escola"
    CURSO_ONLINE = "Curso Online"
    WORKSHOP = "Workshop"
    OUTRO = "Outro"

class TipoEventoEnum(str, enum.Enum):
    AULA = "Aula"
    PROVA = "Prova"
    PALESTRA = "Palestra"
    OUTRO = "Outro"

class StatusRecursoEnum(str, enum.Enum):
    A_FAZER = "A Fazer"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"

class StatusMetaEnum(str, enum.Enum):
    NAO_INICIADA = "Não Iniciada"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

class CategoriaDespesaEnum(str, enum.Enum):
    MENSALIDADE = "Mensalidade"
    MATERIAL = "Material"
    LIVRO = "Livro"
    OUTRO = "Outro"

class EducationInstitution(Base):
    __tablename__ = "education_institutions"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(Enum(TipoInstituicaoEnum), default=TipoInstituicaoEnum.OUTRO)
    descricao = Column(Text, nullable=True)
    eventos = relationship("EducationEvent", back_populates="instituicao")
    certificacoes = relationship("Certification", back_populates="instituicao")

class EducationEvent(Base):
    __tablename__ = "education_events"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(120), nullable=False)
    descricao = Column(Text, nullable=True)
    data_hora = Column(DateTime, nullable=False)
    tipo = Column(Enum(TipoEventoEnum), default=TipoEventoEnum.OUTRO)
    instituicao_id = Column(Integer, ForeignKey("education_institutions.id"))
    instituicao = relationship("EducationInstitution", back_populates="eventos")

class Certification(Base):
    __tablename__ = "certifications"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    instituicao_id = Column(Integer, ForeignKey("education_institutions.id"))
    instituicao = relationship("EducationInstitution", back_populates="certificacoes")
    data_obtencao = Column(Date, nullable=False)
    arquivo = Column(String(255), nullable=True)  # caminho do arquivo digitalizado

class LearningResource(Base):
    __tablename__ = "learning_resources"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(120), nullable=False)
    tipo = Column(String(60), nullable=False)  # livro, curso, artigo, etc.
    status = Column(Enum(StatusRecursoEnum), default=StatusRecursoEnum.A_FAZER)
    observacoes = Column(Text, nullable=True)

class LearningGoal(Base):
    __tablename__ = "learning_goals"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(Text, nullable=False)
    status = Column(Enum(StatusMetaEnum), default=StatusMetaEnum.NAO_INICIADA)
    progresso = Column(Float, default=0.0)  # percentual
    prazo = Column(Date, nullable=True)

class EducationExpense(Base):
    __tablename__ = "education_expenses"
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(120), nullable=False)
    valor = Column(Float, nullable=False)
    data = Column(Date, nullable=False)
    categoria = Column(Enum(CategoriaDespesaEnum), default=CategoriaDespesaEnum.OUTRO)
    observacoes = Column(Text, nullable=True) 