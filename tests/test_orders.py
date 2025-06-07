import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from orders import load_orders, append_order, assign_courier, orders_for_courier


def test_append_and_load(tmp_path):
    csv = tmp_path / "data.csv"
    append_order("Alice", "1 rue A", "Pizza MTP", "Margherita", "12:00", path=csv)
    df = load_orders(csv)
    assert len(df) == 1
    row = df.iloc[0]
    assert row["nom"] == "Alice"
    assert row["plat"] == "Margherita"
    assert row["coursier"] == ""


def test_assign_courier(tmp_path):
    csv = tmp_path / "orders.csv"
    append_order("Bob", "2 rue B", "Tacos Deluxe", "Burrito", "13:00", path=csv)
    assign_courier(0, "Charlie", path=csv)
    df = load_orders(csv)
    assert df.iloc[0]["coursier"] == "Charlie"
    missions = orders_for_courier("Charlie", path=csv)
    assert len(missions) == 1
    assert missions.iloc[0]["nom"] == "Bob"
