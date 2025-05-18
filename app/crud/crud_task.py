from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> List[Task]:
    return db.query(Task).offset(skip).limit(limit).all()

def get_multi_by_user(
    db: Session, *, user_id: int, skip: int = 0, limit: int = 100
) -> List[Task]:
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

def get_multi_by_family(
    db: Session, *, family_id: int, skip: int = 0, limit: int = 100
) -> List[Task]:
    return db.query(Task).filter(Task.family_id == family_id).offset(skip).limit(limit).all()

def create(db: Session, *, obj_in: TaskCreate) -> Task:
    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        due_date=obj_in.due_date,
        completed=obj_in.completed,
        user_id=obj_in.user_id,
        family_id=obj_in.family_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(
    db: Session,
    *,
    db_obj: Task,
    obj_in: TaskUpdate
) -> Task:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, *, task_id: int) -> Task:
    obj = db.query(Task).get(task_id)
    db.delete(obj)
    db.commit()
    return obj 