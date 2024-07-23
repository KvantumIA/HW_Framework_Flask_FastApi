from typing import List
from fastapi import APIRouter
from database.db import database, users
from model.models_user import User, UserIn

router = APIRouter()


@router.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.dict())
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@router.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@router.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(
        **new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@router.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': ' User deleted'}


# Создание фейковых пользователей
@router.get('/fake_users/{count}')
async def create_note(count: int):
    for i in range(1, count + 1):
        query = users.insert().values(first_name=f'Имя_{i}',
                                      last_name=f'Фамилия_{i}',
                                      email=f'mail_{i}@mail.ru',
                                      password='123456')
        await database.execute(query)
    return {'message': f'{count} fake users create'}
