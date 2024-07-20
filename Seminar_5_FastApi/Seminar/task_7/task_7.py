from enum import Enum
from typing import Optional
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
import logging
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

tasks = []
search_id_task = []


class Status(Enum):
    todo = 'поставлена'
    in_progress = 'в процессе'
    done = 'выполнена'


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Status


class TaskIn(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status


@app.get('/tasks/', response_model=list[Task])
async def root():
    logger.info('Вывод всех задач')
    return tasks


@app.post('/tasks/', response_model=list[Task])
async def create_task(new_task: TaskIn):
    tasks.append(Task(id=len(tasks) + 1,
                 title=new_task.title,
                 description=new_task.description,
                 status=new_task.status))
    logger.info('Создание новой задачи')
    return tasks


@app.put('/tasks/', response_model=Task)
async def update_task(task_id: int, new_task: TaskIn):
    for i in range(0, len(tasks)):
        if tasks[i].id == task_id:
            current_task = tasks[task_id - 1]
            current_task.title = new_task.title
            current_task.description = new_task.description
            current_task.status = new_task.status
            logger.info('Изменение задачи')
            return current_task
    raise HTTPException(status_code=404, detail='Task not found')


@app.delete('/tasks/', response_model=dict)
async def delete_task(task_id: int):
    for i in range(0, len(tasks)):
        if tasks[i].id == task_id:
            tasks.remove(tasks[i])
            logger.info('Удаление задачи')
            return {'message': 'Tasks was deleted'}
    raise HTTPException(status_code=404, detail='Task not found')


if __name__ == '__main__':
    uvicorn.run(
        'task_7:app',
        host='127.0.0.1',
        port=8080
    )
