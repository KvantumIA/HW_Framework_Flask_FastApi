from fastapi import FastAPI
import logging
from typing import Optional
from pydantic import BaseModel

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    
@app.get('/')
async def read_root():
    logger.info('Отработал GET запрос')
    return {'message': 'Hello World!'}


@app.post('/items/')
async def create_item(item: Item):
    logger.info('Отработал POST запрос')
    return item


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    logger.info(f'Отработал PUT запрос для item id = {item_id}')
    return {'item_id': item_id, 'item': item}


@app.delete('/items/{item_id}')
async def delete_item(item_id: int):
    logger.info(f'Отработал DELETE запрос для item id = {item_id}')
    return {'item_id': item_id}


