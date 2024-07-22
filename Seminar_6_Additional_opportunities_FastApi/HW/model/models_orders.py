from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class Status(Enum):
    Open_order = 'Открыт'
    Pending = 'В ожидании'
    Processing = 'В обработке'
    Shipped = 'Отправлено'
    Delivered = 'Доставлено'
    Canceled = 'Отменено'


class OrderIn(BaseModel):
    id_user: int = Field(gt=0)
    id_product: int = Field(gt=0)
    date_order: str = Field(max_length=32)
    status: Status

    @field_validator('date_order')
    def validate_date(cls, value):
        try:
            # Попытка преобразовать строку в объект даты
            datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError('date_order must be in the format DD.MM.YYYY')
        return value


class Order(BaseModel):
    id: int
    id_user: int = Field(gt=0)
    id_product: int = Field(gt=0)
    date_order: str = Field(max_length=32)
    status: Status
