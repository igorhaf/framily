import sys
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from app.db.base import Base  # importa todos os modelos
    from app.core.config import settings
except Exception as e:
    print('Erro ao importar modelos ou configurações:')
    traceback.print_exc()
    sys.exit(1)

print('Testando inicialização dos mapeamentos do SQLAlchemy...')

try:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(bind=engine)
    print('Mapeamento dos modelos inicializado com sucesso!')
except Exception as e:
    print('Erro ao inicializar mapeamento dos modelos:')
    traceback.print_exc()
    sys.exit(1) 