from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from datetime import datetime

from .database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    adresse = Column(String)
    restaurant = Column(String)
    plat = Column(String)
    heure = Column(String)
    coursier = Column(String, nullable=True)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())


class OrderCreate(BaseModel):
    nom: str
    adresse: str
    restaurant: str
    plat: str
    heure: str


class OrderAssign(BaseModel):
    coursier: str


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String, nullable=True)


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    amount = Column(Float, nullable=True)
    status = Column(String, default="pending")


class PaymentCreate(BaseModel):
    order_id: int
    amount: float | None = None
