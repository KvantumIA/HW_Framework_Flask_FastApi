import random
from typing import List
from fastapi import APIRouter, HTTPException
from database.db import database, orders, users, products
from model.models_orders import Order, OrderIn, Status
from sqlalchemy import select

router_order = APIRouter()


@router_order.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.dict())
    last_record_id = await database.execute(query)
    return {**order.dict(), 'id': last_record_id}


@router_order.get('/orders/', response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router_order.get('/orders/{product_id}')
async def read_order(order_id: int):
    query = select(orders.c.id, orders.c.date_order, orders.c.status,
                   products.c.id.label('product_id'), products.c.name, products.c.description, products.c.price,
                   users.c.id.label('user_id'), users.c.first_name, users.c.last_name, users.c.email).join(products).join(users).where(orders.c.id == order_id)
    rows = await database.fetch_all(query)
    if rows is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return rows


@router_order.put('/orders/{product_id}', response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(
        **new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), 'id': order_id}


@router_order.delete('/orders/{product_id}')
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}


# async def fake_date():
#     return f'{random.randint(1, 31)}.{random.randint(1, 12)}.2024'


# Создание фейковых заказов
@router_order.get('/fake_orders/{count}')
async def create_fake_order(count: int):
    choise = ['Open_order', 'Pending', 'Processing', 'Shipped', 'Delivered',
                'Canceled']
    for i in range(1, count + 1):
        query = orders.insert().values(id_user=random.randint(1, 10),
                                       id_product=random.randint(1, 10),
                                       date_order=f'{random.randint(1, 31)}.{random.randint(1, 12)}.2024',
                                       status=random.choice(choise))
        await database.execute(query)
    return {'message': f'{count} fake orders create'}

