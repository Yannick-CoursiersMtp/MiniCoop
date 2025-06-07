from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Header,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from . import models, database

app = FastAPI(title="MiniCoop API")

database.init_db()

security = HTTPBasic()
ACCESS_TOKEN = "secrettoken"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_token(token: str = Header(None, alias="X-Token")):
    if token != ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    username_match = secrets.compare_digest(credentials.username, "alice")
    password_match = secrets.compare_digest(credentials.password, "wonderland")
    if not (username_match and password_match):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"token": ACCESS_TOKEN}


@app.post("/orders", response_model=dict)
def create_order(
    order: models.OrderCreate,
    db: Session = Depends(get_db),
    token: str = Depends(require_token),
):
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
def list_orders(
    db: Session = Depends(get_db), token: str = Depends(require_token)
):
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
def assign_courier(
    order_id: int,
    assignment: models.OrderAssign,
    db: Session = Depends(get_db),
    token: str = Depends(require_token),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.coursier = assignment.coursier
    db.commit()
    return {"status": "assigned"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        pass
