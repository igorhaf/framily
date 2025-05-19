from .tasks import router as tasks_router
from .finance import router as finance_router
from .health import router as health_router

tasks = tasks_router
finance = finance_router
health = health_router

__all__ = ["tasks", "finance", "health"] 