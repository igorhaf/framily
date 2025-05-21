from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api import deps
import logging
import traceback

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve tasks.
    """
    try:
        logger.info("Iniciando busca de tarefas...")
        logger.info(f"Parâmetros: skip={skip}, limit={limit}")
        
        tasks = crud.task.get_multi(db, skip=skip, limit=limit)
        logger.info(f"Tarefas encontradas: {len(tasks)}")
        
        # Log das tarefas encontradas
        for task in tasks:
            logger.info(f"Tarefa ID: {task.id}, Título: {task.title}, Status: {task.status}")
        
        return tasks
    except Exception as e:
        logger.error(f"Erro ao buscar tarefas: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error while retrieving tasks: {str(e)}"
        )

@router.post("/", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.TaskCreate,
):
    """
    Create new task.
    """
    try:
        task = crud.task.create(db=db, obj_in=task_in)
        logger.info(f"Created task with ID: {task.id}")
        return task
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while creating task"
        ) 