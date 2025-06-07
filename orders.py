"""Utility functions for managing orders stored in a CSV file.

This module centralizes the CSV operations used across the Streamlit
interfaces. It provides helpers to load all orders, append a new one
and assign a courier.
"""

import pandas as pd
from datetime import datetime

FILE_PATH = "data.csv"
COLUMNS = ["nom", "adresse", "restaurant", "plat", "heure", "coursier", "timestamp"]

def read_orders():
    """Return all orders as a DataFrame, or an empty DataFrame if none."""
    try:
        return pd.read_csv(FILE_PATH, names=COLUMNS)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(columns=COLUMNS)

def append_order(order):
    """Append a single order dictionary to the CSV file."""
    df = pd.DataFrame([order])
    df.to_csv(FILE_PATH, mode="a", header=False, index=False)

def assign_courier(timestamp: str, courier: str):
    """Assign a courier to the order identified by its timestamp."""
    orders = read_orders()
    mask = orders["timestamp"] == timestamp
    if mask.any():
        orders.loc[mask, "coursier"] = courier
        orders.to_csv(FILE_PATH, index=False, header=False)
