from .tasks import router as tasks_router
from .finance import router as finance_router
from .health import router as health_router
from .calendar import router as calendar_router
from .shopping import router as shopping_router
from .whatsapp import router as whatsapp_router

tasks = tasks_router
finance = finance_router
health = health_router
calendar = calendar_router
shopping = shopping_router
whatsapp = whatsapp_router

__all__ = ["tasks", "finance", "health", "calendar", "shopping", "whatsapp"] 