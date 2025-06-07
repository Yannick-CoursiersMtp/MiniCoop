from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, database

app = FastAPI(title="MiniCoop API")

database.init_db()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/orders", response_model=dict)
def create_order(order: models.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        nom=order.nom,
        adresse=order.adresse,
        restaurant=order.restaurant,
        plat=order.plat,
        heure=order.heure,
        coursier="",
        timestamp=datetime.now().isoformat(),
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"id": db_order.id, "timestamp": db_order.timestamp}


@app.get("/orders", response_model=list[dict])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return [
        {
            "id": o.id,
            "nom": o.nom,
            "adresse": o.adresse,
            "restaurant": o.restaurant,
            "plat": o.plat,
            "heure": o.heure,
            "coursier": o.coursier,
            "timestamp": o.timestamp,
        }
        for o in orders
    ]


@app.put("/orders/{order_id}/assign")
def assign_courier(order_id: int, assignment: models.OrderAssign, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.coursier = assignment.coursier
    db.commit()
    return {"status": "assigned"}
