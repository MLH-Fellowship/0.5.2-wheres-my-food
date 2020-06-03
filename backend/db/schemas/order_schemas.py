from pydantic import BaseModel
from typing import List


class OrderBase(BaseModel):
    status: int
    user_email: str
    order_id: int


class OrderCreate(OrderBase):
    platform_id: int


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True
