# MiniCoop

Small prototype of a delivery service built with Streamlit.

## Modules

- `client.py` – allows customers to place orders.
- `admin.py` – admin dashboard to view and assign couriers.
- `coursier.py` – interface for couriers to see their deliveries.
- `resto.py` – restaurant view of incoming orders.
- `orders.py` – helper functions to read/write orders CSV.

## Installation

1. Install Python 3.11 or later.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run any of the Streamlit apps. For example:
```bash
streamlit run client.py
```
Replace `client.py` with `admin.py`, `coursier.py`, or `resto.py` for the other interfaces.

## Running Tests

Execute the test suite with:
```bash
pytest -q
```
