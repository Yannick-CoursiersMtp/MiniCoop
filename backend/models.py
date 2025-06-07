from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
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


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    amount = Column(Integer)
    status = Column(String)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())


class PaymentCreate(BaseModel):
    order_id: int
    amount: int
    status: str
