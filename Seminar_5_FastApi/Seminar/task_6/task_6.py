import random
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

users = []
search_id_user = []


class UserOut(BaseModel):
    id: int
    name: str
    email: str


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(UserIn):
    id: int


# def fill_users():
for i in range(1, 11):
    users.append(User(
        id=i,
        name=f'Name_{i}',
        email=f'email{i}@mail.ru',
        password=str(random.randint(123, 12345))
    ))


@app.get('/', response_class=HTMLResponse)
async def base(request: Request):
    """
    Переход на главную страницу
    """
    return templates.TemplateResponse("users.html",
                                      {"request": request, 'title': 'Главная'})


@app.get('/main/', response_class=HTMLResponse)
async def main(request: Request):
    """
    Переход на главную страницу
    """
    return templates.TemplateResponse("users.html",
                                      {"request": request, 'title': 'Главная'})


# -------------------------------------------------------------------
@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    """
    Вывод списка всех пользователей
    """
    logger.info(f'Распечатан список пользователей')
    return templates.TemplateResponse("users.html",
                                      {"request": request, "users": users,
                                       'title': 'Список Users'})


# -------------------------------------------------------------------
@app.get("/create_user/", response_class=HTMLResponse)
async def get_create_user(request: Request):
    """
    GET запрос для добавления нового пользователя
    """
    return templates.TemplateResponse("create_user.html", {"request": request, 'title': 'Добавление пользователя', 'action': '/create_user/'})


@app.post("/create_user/")
async def post_create_user(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """
    POST запрос для добавления нового пользователя
    """
    users.append(User(id=len(users) + 1,
                      name=username,
                      email=email,
                      password=password))
    logger.info(f'Пользователь {username} добавлен!')
    return templates.TemplateResponse("main.html", {"request": request, 'title': 'Главная', 'message': 'Добавлен новый пользователь!'})


# -------------------------------------------------------------------
@app.get("/search_user/", response_class=HTMLResponse)
async def get_search_user(request: Request):
    """
    GET запрос ддя Поиска пользователя
    """
    return templates.TemplateResponse("search_user.html", {"request": request, 'title': 'Поиск пользователя'})


@app.post("/search_user/")
async def post_search_user(request: Request, user_id: int = Form(...)):
    """
    POST запрос для Поиска пользователя
    """
    global search_id_user
    for user in users:
        if user_id == user.id:
            search_id_user = [user]
            logger.info(f'Пользователь {user.name} найден!')
            return templates.TemplateResponse("users.html", {"request": request, 'title': 'Поиск пользователя', 'users': search_id_user, 'edit_user': 'yes'})
    raise HTTPException(status_code=404, detail='Пользователь не найден')


# -------------------------------------------------------------------
@app.post("/edit_user/", response_class=HTMLResponse)
async def post_edit_user(request: Request):
    """
    Изменение пользователя
    """
    return templates.TemplateResponse("create_user.html", {"request": request, 'title': 'Изменение пользователя', 'action': '/edit_user_2/'})


@app.post('/edit_user_2/')
async def post_edit_user_2(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    """
    Изменение пользователя
    """
    for user in users:
        if search_id_user[0].id == user.id:
            # current_user = search_id_user[0]
            user.name = username
            user.email = email
            user.password = password
            logger.info(f'Отработал PUT запрос для изменения пользователя {search_id_user[0].name}')
            return templates.TemplateResponse("main.html", {"request": request, 'title': 'Главная', 'message': f'Пользователь {search_id_user[0].name} изменен!'})


# -------------------------------------------------------------------
@app.post('/delete_user/', response_model=dict)
@app.delete('/delete_user/', response_model=dict)
async def delete_user(request: Request,):
    """
    Удаление пользователя
    """
    for user in users:
        if search_id_user[0].id == user.id:
            users.remove(user)
            logger.info('Отработал DELETE запрос')
            return templates.TemplateResponse("main.html", {"request": request, 'title': 'Главная', 'message': f'Пользователь {search_id_user[0].name} удален!'})


if __name__ == '__main__':
    uvicorn.run(
        'task_6:app',
        host='127.0.0.1',
        port=8080
    )
