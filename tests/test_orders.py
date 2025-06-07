from datetime import datetime
from orders import load_orders, append_order, update_status

def test_append_order(tmp_path):
    csv = tmp_path / "data.csv"
    order = {
        "nom": "Alice",
        "adresse": "1 rue",
        "restaurant": "Pizza MTP",
        "plat": "pizza",
        "heure": "12:00",
        "coursier": "",
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }
    append_order(order, path=csv)
    df = load_orders(path=csv)
    assert len(df) == 1
    assert df.iloc[0]["nom"] == "Alice"

def test_assign_coursier(tmp_path):
    csv = tmp_path / "data.csv"
    ts = datetime.now().isoformat()
    order = {
        "nom": "Bob",
        "adresse": "2 rue",
        "restaurant": "Tacos Deluxe",
        "plat": "tacos",
        "heure": "13:00",
        "coursier": "",
        "timestamp": ts,
        "status": "pending",
    }
    append_order(order, path=csv)
    update_status(ts, path=csv, coursier="John")
    df = load_orders(path=csv)
    assert df.iloc[0]["coursier"] == "John"

def test_mark_ready(tmp_path):
    csv = tmp_path / "data.csv"
    ts = datetime.now().isoformat()
    order = {"nom": "Eve", "adresse": "3 rue", "restaurant": "Vegan Bowl", "plat": "bowl", "heure": "14:00", "coursier": "", "timestamp": ts, "status": "pending"}
    append_order(order, path=csv)
    update_status(ts, path=csv, status="ready")
    df = load_orders(path=csv)
    assert df.iloc[0]["status"] == "ready"

def test_mark_delivered(tmp_path):
    csv = tmp_path / "data.csv"
    ts = datetime.now().isoformat()
    order = {"nom": "Dan", "adresse": "4 rue", "restaurant": "Pizza MTP", "plat": "pizza", "heure": "15:00", "coursier": "Paul", "timestamp": ts, "status": "ready"}
    append_order(order, path=csv)
    update_status(ts, path=csv, status="delivered")
    df = load_orders(path=csv)
    assert df.iloc[0]["status"] == "delivered"
