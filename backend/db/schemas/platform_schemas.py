from pydantic import BaseModel
from typing import List
from db.schemas.order_schemas import Order


class PlatformBase(BaseModel):
    name: str


class PlatformCreate(PlatformBase):
    pass


class Platform(PlatformBase):
    id: int

    orders: List[Order] = []

    class Config:
        orm_mode = True
