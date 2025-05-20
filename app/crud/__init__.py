from .crud_task import Task
from .base import CRUDBase
from app.models.task import Task as TaskModel
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.crud_shopping import shopping_list, shopping_item

task = CRUDBase[TaskModel, TaskCreate, TaskUpdate](TaskModel)

__all__ = ["task", "shopping_list", "shopping_item"] 