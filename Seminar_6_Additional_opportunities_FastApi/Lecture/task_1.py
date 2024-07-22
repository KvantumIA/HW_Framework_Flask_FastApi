from typing import List
import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = 'sqlite:///my_database.database'
# DATABASE_URL = 'postgresql://user:password@localhost/dbname'

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer,
                                           primary_key=True),
                         sqlalchemy.Column('name', sqlalchemy.String(32)),
                         sqlalchemy.Column('email', sqlalchemy.String(128)),
                         )

engine = sqlalchemy.create_engine(DATABASE_URL,
                                  connect_args={'check_same_thread': False})

metadata.create_all(engine)

app = FastAPI()


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    email: str = Field(max_length=128)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# @app.get('/fake_users/{count}')
# async def create_note(count: int):
#     for i in range(1, count+1):
#         query = users.insert().values(name=f'user{i}',
#                                       email=f'mail{i}@mail.ru')
#         await database.execute(query)
#     return {'message': f'{count} fake users create'}

@app.post('/users/', response_model=User)
async def create_user(user: User):
    query = users.insert().values(name=user.name, email=user.email)   # два разных варианта заполнения
    query = users.insert().values(**user.dict())                   # два разных варианта заполнения
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), 'id': user_id}


@app.delete('/users/{user_id}')
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': ' User deleted'}


if __name__ == '__main__':
    uvicorn.run(
        'task_1:app',
        host='127.0.0.1',
        port=8080
    )
