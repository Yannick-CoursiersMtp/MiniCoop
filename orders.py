from typing import Dict
import pandas as pd

COLUMNS = [
    "nom",
    "adresse",
    "restaurant",
    "plat",
    "heure",
    "coursier",
    "timestamp",
    "status",
]

def load_orders(path: str = "data.csv") -> pd.DataFrame:
    """Return the orders dataframe, creating an empty one if needed."""
    try:
        df = pd.read_csv(path, names=COLUMNS)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUMNS)
    return df

def append_order(order: Dict[str, str], path: str = "data.csv") -> None:
    """Append a single order to the CSV file."""
    df = pd.DataFrame([order])
    df.to_csv(path, mode="a", header=False, index=False)

def update_status(timestamp: str, path: str = "data.csv", **updates: str) -> None:
    """Update fields for the order matching the timestamp."""
    df = load_orders(path)
    mask = df["timestamp"] == timestamp
    for key, value in updates.items():
        if key in df.columns:
            df.loc[mask, key] = value
    df.to_csv(path, index=False, header=False)
