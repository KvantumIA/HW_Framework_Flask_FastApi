import random
from typing import List
from fastapi import APIRouter
from database.db import database, products
from model.models_products import Product, ProductIn

router_product = APIRouter()


@router_product.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values( **product.dict())
    last_record_id = await database.execute(query)
    return {**product.dict(), 'id': last_record_id}


@router_product.get('/products/', response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@router_product.get('/products/{product_id}', response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@router_product.put('/products/{product_id}', response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(
        **new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), 'id': product_id}


@router_product.delete('/products/{product_id}')
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {'message': 'Product deleted'}


# Создание фейковых продуктов
@router_product.get('/fake_products/{count}')
async def create_fake_product(count: int):
    for i in range(1, count + 1):
        query = products.insert().values(name=f'Название_{i}',
                                         description=f'Описание_{i}',
                                         price=random.randint(1000, 10000))
        await database.execute(query)
    return {'message': f'{count} fake products create'}
