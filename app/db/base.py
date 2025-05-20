# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.family import Family, FamilyMember  # noqa
from app.models.task import Task  # noqa
from app.models.event import Event  # noqa
from app.models.finance import FinanceCategory, FinanceTransaction, FinanceBudget  # noqa
from app.models.health import HealthAppointment, HealthMedication, HealthExam  # noqa
from app.models.calendar import CalendarEvent  # noqa
from app.models.shopping import ShoppingList, ShoppingItem  # noqa

# Importar todos os modelos aqui para que o Alembic os detecte
__all__ = ["Base", "CalendarEvent", "ShoppingList", "ShoppingItem"] 