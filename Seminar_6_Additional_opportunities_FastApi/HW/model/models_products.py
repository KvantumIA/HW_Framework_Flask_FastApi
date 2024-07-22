from pydantic import BaseModel, Field, EmailStr


class ProductIn(BaseModel):
    name: str = Field(..., max_length=128)
    description: str = Field(None, max_length=128)
    price: int = Field(..., gt=1)


class Product(BaseModel):
    id: int
    name: str = Field(..., max_length=128)
    description: str = Field(None, max_length=128)
    price: int = Field(..., gt=1)
