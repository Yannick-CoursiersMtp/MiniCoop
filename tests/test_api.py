import os
from fastapi.testclient import TestClient

# use a temporary database file for tests
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
if os.path.exists("test.db"):
    os.remove("test.db")

from backend.main import app  # noqa: E402
from backend.database import init_db  # noqa: E402

client = TestClient(app)
init_db()


def teardown_module(module):
    if os.path.exists("test.db"):
        os.remove("test.db")


def login_token():
    response = client.post("/login", auth=("alice", "wonderland"))
    assert response.status_code == 200
    return response.json()["token"]


def test_create_list_assign():
    token = login_token()
    headers = {"X-Token": token}
    order = {
        "nom": "John",
        "adresse": "1 rue A",
        "restaurant": "Pizza MTP",
        "plat": "Margherita",
        "heure": "12:00",
    }
    r = client.post("/orders", json=order, headers=headers)
    assert r.status_code == 200
    order_id = r.json()["id"]

    r = client.get("/orders", headers=headers)
    assert r.status_code == 200
    ids = [o["id"] for o in r.json()]
    assert order_id in ids

    r = client.put(f"/orders/{order_id}/assign", json={"coursier": "Bob"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["status"] == "assigned"


def test_authentication_required():
    order = {
        "nom": "Jane",
        "adresse": "2 rue B",
        "restaurant": "Pizza MTP",
        "plat": "Veggie",
        "heure": "13:00",
    }
    r = client.post("/orders", json=order)
    assert r.status_code == 401
    r = client.get("/orders")
    assert r.status_code == 401


def test_websocket_echo():
    with client.websocket_connect("/ws") as ws:
        ws.send_text("ping")
        data = ws.receive_text()
        assert data == "pong"
