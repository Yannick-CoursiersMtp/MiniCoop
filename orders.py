import pandas as pd
from datetime import datetime
from pathlib import Path

COLUMNS = ["nom", "adresse", "restaurant", "plat", "heure", "coursier", "timestamp"]


def load_orders(path: str = "data.csv") -> pd.DataFrame:
    """Load orders from CSV. Return empty DataFrame if file missing."""
    file = Path(path)
    if not file.exists():
        return pd.DataFrame(columns=COLUMNS)
    df = pd.read_csv(file, names=COLUMNS, dtype=str)
    return df.fillna("")


def append_order(nom: str, adresse: str, restaurant: str, plat: str, heure: str,
                 path: str = "data.csv", *, timestamp: str | None = None) -> None:
    """Append a new order to the CSV."""
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    df = pd.DataFrame([{"nom": nom,
                        "adresse": adresse,
                        "restaurant": restaurant,
                        "plat": plat,
                        "heure": heure,
                        "coursier": "",
                        "timestamp": timestamp}])
    df.to_csv(path, mode="a", header=False, index=False)


def assign_courier(index: int, coursier: str, path: str = "data.csv") -> pd.DataFrame:
    """Assign a courier to an order and return updated DataFrame."""
    orders = load_orders(path)
    if index < 0 or index >= len(orders):
        raise IndexError("Invalid order index")
    orders.at[index, "coursier"] = coursier
    orders.to_csv(path, index=False, header=False)
    return orders


def orders_for_courier(coursier: str, path: str = "data.csv") -> pd.DataFrame:
    """Return orders assigned to the given courier."""
    orders = load_orders(path)
    return orders[orders["coursier"] == coursier]
