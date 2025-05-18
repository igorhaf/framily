from .users import router as users_router
from .tasks import router as tasks_router
from .calendar import router as calendar_router
from .finances import router as finances_router
from .health import router as health_router

users = users_router
tasks = tasks_router
calendar = calendar_router
finances = finances_router
health = health_router

__all__ = ["users", "tasks", "calendar", "finances", "health"] 