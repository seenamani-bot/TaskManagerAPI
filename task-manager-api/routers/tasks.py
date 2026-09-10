from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router=APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    class TaskCreate(BaseModel):
        title: str
    completed: bool = False
    notes: str = ""
    priority: str = "normal"
    
    
tasks = [
    {"id": 1, "title": "Learn FastAPI", "completed": False},
    {"id": 2, "title": "Buy groceries", "completed": True},
    {"id": 3, "title": "Walk the dog", "completed": False},
]
    
    

@router.get("")
def list_tasks(completed: bool | None = None, search:str | None =None):
    result=tasks
    if completed is not None:
        result=[t for t in result if t["completed"]==completed]
    if search is not None:
        result=[t for t in result if search.casefold() in t["title"].casefold()]
    return result

@router.get("/{task_id}")
def get_tasks(task_id:int):
    for t in tasks:
        if t["id"]==task_id:
         return t
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}")
def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.post("", status_code=201)
def create_task(task: TaskCreate):
    new_id = max((t["id"] for t in tasks), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "completed": task.completed,
        "notes": task.notes,
        "priority": task.priority,
    }
    tasks.append(new_task)
    return new_task
       
        