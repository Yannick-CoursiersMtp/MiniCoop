from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)


class UserCreate(BaseModel):
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str
