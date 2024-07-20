import uvicorn
from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    status: str


@app.get('/tasks/', response_model=list[Task])
async def root():
    logger.info('Отработал GET запрос tasks')
    return tasks


@app.post('/tasks/', response_model=list[Task])
async def create_task(new_task: TaskIn):
    tasks.append(Task(id=len(tasks) + 1,
                 title=new_task.title,
                 description=new_task.description,
                 status=new_task.status))
    logger.info('Отработал POST запрос')
    return tasks


@app.put('/tasks/', response_model=Task)
async def edit_task(task_id: int, new_task: TaskIn):
    for i in range(0, len(tasks)):
        if tasks[i].id == task_id:
            current_task = tasks[task_id - 1]
            current_task.title = new_task.title
            current_task.description = new_task.description
            current_task.status = new_task.status
            logger.info('Отработал PUT запрос')
            return current_task
    raise HTTPException(status_code=404, detail='Task not found')


@app.delete('/tasks/', response_model=dict)
async def delete_task(task_id: int):
    for i in range(0, len(tasks)):
        if tasks[i].id == task_id:
            tasks.remove(tasks[i])
            logger.info('Отработал DELETE запрос')
            return {'message': 'Tasks was deleted'}
    raise HTTPException(status_code=404, detail='Task not found')


if __name__ == '__main__':
    uvicorn.run(
        'task_1:app',
        host='127.0.0.1',
        port=8080
    )
