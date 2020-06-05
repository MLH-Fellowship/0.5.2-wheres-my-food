
from sqlalchemy.orm import Session
from db.schemas.user_schemas import UserCreate
from db.schemas.order_schemas import OrderCreate
from db.models import User, Order
from auth.auth_utils import get_password_hash

def create_user(db: Session, user: UserCreate):
    user.password = get_password_hash(user.password)
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_users_orders(db: Session, email:str, skip: int = 0, limit: int = 100):
    return db.query(Order).filter(Order.user_email == email).offset(skip).limit(limit).all()

def create_user_order(db: Session, order:OrderCreate):
    db_item = Order(**order.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_order_by_foreign_id(db: Session, order_id: str, platform_id: int):
    return db.query(Order).filter(Order.order_id == order_id, Order.platform_id == platform_id).first()


def update_user_order(db: Session, order_id: str, platform_id:int, new_status: int):
    order = db.query(Order).filter(Order.order_id == order_id, Order.platform_id == platform_id).first()
    order.status = new_status
    db.add(order)
    db.commit()
    return order

