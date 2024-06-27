from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    mobile = Column(String, index=True, unique=True)
    age = Column(Integer, nullable=True)
    active = Column(Boolean, default=True)
    status = Column(Enum("ACTIVE", "INACTIVE"), default="ACTIVE")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
