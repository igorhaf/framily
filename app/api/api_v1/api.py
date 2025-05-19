from fastapi import APIRouter

api_router = APIRouter()

# Import routers from endpoints
from app.api.api_v1.endpoints.users import router as users_router
from app.api.api_v1.endpoints.tasks import router as tasks_router
from app.api.api_v1.endpoints.calendar import router as calendar_router
from app.api.api_v1.endpoints.finances import router as finances_router
from app.api.api_v1.endpoints.health import router as health_router
from app.api.api_v1.endpoints import finance

# User management
api_router.include_router(users_router, prefix="/users", tags=["users"])

# Task management
api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

# Calendar management
api_router.include_router(calendar_router, prefix="/calendar", tags=["calendar"])

# Financial management
api_router.include_router(finances_router, prefix="/finances", tags=["finances"])

# Health tracking
api_router.include_router(health_router, prefix="/health", tags=["health"])

api_router.include_router(finance.router, prefix="/finance", tags=["finance"]) 