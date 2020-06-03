from pydantic import BaseModel
from typing import List
from db.schemas.order_schemas import Order


class UserBase(BaseModel):
    full_name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    orders: List[Order] = []
    is_admin: bool = False

    class Config:
        orm_mode = True
