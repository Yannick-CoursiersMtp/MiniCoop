from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import hashlib

from . import models, database

app = FastAPI(title="MiniCoop API")

database.init_db()

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    if user_id is None:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


def require_role(role: str):
    def role_dependency(user: models.User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return role_dependency


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/register")
def register(user: models.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = models.User(email=user.email, password_hash=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login")
def login(credentials: models.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/orders", response_model=dict)
def create_order(
    order: models.OrderCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_role("client")),
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
    db: Session = Depends(get_db),
    user: models.User = Depends(require_role("admin")),
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
    user: models.User = Depends(require_role("admin")),
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.coursier = assignment.coursier
    db.commit()
    return {"status": "assigned"}
