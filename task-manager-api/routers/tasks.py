from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Field, SQLModel, Session, select

from db import get_session

router = APIRouter(prefix="/tasks", tags=["tasks"])


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    completed: bool = False
    notes: str = ""
    priority: str = "normal"


@router.get("")
def list_tasks(completed: bool | None = None, search: str | None = None, session: Session = Depends(get_session)):
    query = select(Task)
    if completed is not None:
        query = query.where(Task.completed == completed)
    results = session.exec(query).all()
    if search is not None:
        results = [t for t in results if search.casefold() in t.title.casefold()]
    return results


@router.get("/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
        task = session.get(Task, task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
@router.post("", status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int,session: Session = Depends(get_session) ):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"message": "Task deleted"}