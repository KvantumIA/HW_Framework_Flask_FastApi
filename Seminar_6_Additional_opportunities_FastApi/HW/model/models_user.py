from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    email: EmailStr = Field(..., max_length=128)
    password: str = Field(..., min_length=6)


class User(BaseModel):
    id: int
    first_name: str = Field(..., max_length=32)
    last_name: str = Field(..., max_length=32)
    email: EmailStr = Field(..., max_length=128)
    # password: str = Field(min_length=6)
