from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from enum import Enum

class TipoInstituicaoEnum(str, Enum):
    FACULDADE = "Faculdade"
    ESCOLA = "Escola"
    CURSO_ONLINE = "Curso Online"
    WORKSHOP = "Workshop"
    OUTRO = "Outro"

class TipoEventoEnum(str, Enum):
    AULA = "Aula"
    PROVA = "Prova"
    PALESTRA = "Palestra"
    OUTRO = "Outro"

class StatusRecursoEnum(str, Enum):
    A_FAZER = "A Fazer"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluído"

class StatusMetaEnum(str, Enum):
    NAO_INICIADA = "Não Iniciada"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDA = "Concluída"

class CategoriaDespesaEnum(str, Enum):
    MENSALIDADE = "Mensalidade"
    MATERIAL = "Material"
    LIVRO = "Livro"
    OUTRO = "Outro"

class EducationInstitutionBase(BaseModel):
    nome: str
    tipo: TipoInstituicaoEnum = TipoInstituicaoEnum.OUTRO
    descricao: Optional[str] = None

class EducationInstitutionCreate(EducationInstitutionBase):
    pass

class EducationInstitutionInDB(EducationInstitutionBase):
    id: int
    class Config:
        from_attributes = True

class EducationEventBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_hora: datetime
    tipo: TipoEventoEnum = TipoEventoEnum.OUTRO
    instituicao_id: Optional[int] = None

class EducationEventCreate(EducationEventBase):
    pass

class EducationEventInDB(EducationEventBase):
    id: int
    class Config:
        from_attributes = True

class CertificationBase(BaseModel):
    nome: str
    instituicao_id: Optional[int] = None
    data_obtencao: date
    arquivo: Optional[str] = None

class CertificationCreate(CertificationBase):
    pass

class CertificationInDB(CertificationBase):
    id: int
    class Config:
        from_attributes = True

class LearningResourceBase(BaseModel):
    titulo: str
    tipo: str
    status: StatusRecursoEnum = StatusRecursoEnum.A_FAZER
    observacoes: Optional[str] = None

class LearningResourceCreate(LearningResourceBase):
    pass

class LearningResourceInDB(LearningResourceBase):
    id: int
    class Config:
        from_attributes = True

class LearningGoalBase(BaseModel):
    descricao: str
    status: StatusMetaEnum = StatusMetaEnum.NAO_INICIADA
    progresso: float = 0.0
    prazo: Optional[date] = None

class LearningGoalCreate(LearningGoalBase):
    pass

class LearningGoalInDB(LearningGoalBase):
    id: int
    class Config:
        from_attributes = True

class EducationExpenseBase(BaseModel):
    descricao: str
    valor: float
    data: date
    categoria: CategoriaDespesaEnum = CategoriaDespesaEnum.OUTRO
    observacoes: Optional[str] = None

class EducationExpenseCreate(EducationExpenseBase):
    pass

class EducationExpenseInDB(EducationExpenseBase):
    id: int
    class Config:
        from_attributes = True 