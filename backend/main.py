from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from . import models, database

app = FastAPI(title="MiniCoop API")

database.init_db()


# Keep track of connected websockets per order
order_connections: dict[int, set[WebSocket]] = {}

async def broadcast(order_id: int, message: dict):
    """Send a message to all websockets listening for this order."""
    connections = list(order_connections.get(order_id, set()))
    for ws in connections:
        try:
            await ws.send_json(message)
        except Exception:
            # Drop broken connections silently
            order_connections[order_id].discard(ws)


@app.websocket("/ws/orders/{order_id}")
async def order_updates(websocket: WebSocket, order_id: int):
    await websocket.accept()
    order_connections.setdefault(order_id, set()).add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        order_connections[order_id].discard(websocket)



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/orders", response_model=dict)
async def create_order(order: models.OrderCreate, db: Session = Depends(get_db)):
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
    await broadcast(db_order.id, {"event": "created", "id": db_order.id})
    return {"id": db_order.id, "timestamp": db_order.timestamp}


@app.get("/orders", response_model=list[dict])
async def list_orders(db: Session = Depends(get_db)):
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
            "ready": o.ready,
        }
        for o in orders
    ]


@app.put("/orders/{order_id}/assign")
async def assign_courier(order_id: int, assignment: models.OrderAssign, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.coursier = assignment.coursier
    db.commit()
    await broadcast(order_id, {"event": "assigned", "courier": assignment.coursier})
    return {"status": "assigned"}


@app.put("/orders/{order_id}/ready")
async def mark_ready(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.ready = True
    db.commit()
    await broadcast(order_id, {"event": "ready"})
    return {"status": "ready"}
