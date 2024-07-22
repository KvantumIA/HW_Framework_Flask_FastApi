import uvicorn
from fastapi import FastAPI
from Seminar_6_Additional_opportunities_FastApi.HW.database.db import database
from Seminar_6_Additional_opportunities_FastApi.HW.data import user, product, order

app = FastAPI()


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
        host='127.0.0.1',
        port=8080,
        reload=True
    )
