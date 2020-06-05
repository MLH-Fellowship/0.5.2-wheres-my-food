from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=True)
    password = Column(String)

    orders = relationship("Order", backref="users")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, index=True)  # Platform order id
    platform_id = Column(Integer, ForeignKey("platforms.id"))
    status = Column(Integer, default=0)
    user_email = Column(String, ForeignKey("users.email"))


class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    orders = relationship("Order", backref="platforms")
