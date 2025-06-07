from fastapi.testclient import TestClient

from backend.main import app
from backend.database import Base, engine


# Ensure a fresh database for each test run
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_create_payment_via_api():
    order_payload = {
        "nom": "Test",
        "adresse": "123 Street",
        "restaurant": "Pizza MTP",
        "plat": "Margherita",
        "heure": "12:00",
    }
    response = client.post("/orders", json=order_payload)
    assert response.status_code == 200
    order_id = response.json()["id"]

    payment_payload = {"order_id": order_id, "amount": 15.5}
    response = client.post("/payments", json=payment_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "paid"
