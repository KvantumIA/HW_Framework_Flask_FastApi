import uvicorn
from fastapi import FastAPI
from database.db import database
from data import user, product, order
from settings.settings import settings

app = FastAPI()
HOST = settings.HOST
PORT = settings.PORT


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


app.include_router(user.router, tags=['users'])
app.include_router(product.router_product, tags=['products'])
app.include_router(order.router_order, tags=['orders'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=HOST,
        port=PORT,
        reload=True
    )
