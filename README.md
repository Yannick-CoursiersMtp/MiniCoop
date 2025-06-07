# MiniCoop

This repository contains simple Streamlit apps for managing fictional delivery operations. All scripts rely on the shared `data.csv` file to record and read orders.

## Scripts

- **client.py** - Interface for customers to place an order. Appends a new entry to `data.csv`.
- **resto.py** - Restaurant view listing orders for a selected restaurant.
- **admin.py** - Administrative interface to assign couriers to orders.
- **coursier.py** - Courier interface showing deliveries assigned to the logged-in courier.

## Running the apps

Each script can be launched with Streamlit. From the repository root run:

```bash
streamlit run client.py
streamlit run resto.py
streamlit run admin.py
streamlit run coursier.py
```

All apps expect `data.csv` to exist in the same directory. The provided `data.csv` is an empty placeholder that will be populated after the first order is created.
