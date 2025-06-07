# MiniCoop

MiniCoop is a small demonstration of a food delivery workflow built with [Streamlit](https://streamlit.io/). The project contains four standalone Streamlit applications representing the actors of the workflow:

- **Client** (`client.py`) – form allowing customers to place an order.
- **Admin** (`admin.py`) – interface for dispatching every order to a courier.
- **Coursier** (`coursier.py`) – dashboard where a courier sees the orders assigned to them.
- **Restaurant** (`resto.py`) – view of pending orders for a particular restaurant.

All applications read from or write to the shared file `data.csv`, which stores the order information. There is no authentication and the data only lives inside this CSV file, so the project is intended for local demonstrations.

## Installation

Install the dependencies with `pip` using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Streamlit apps

Launch any of the interfaces with `streamlit run` followed by the desired script. For example, to open the restaurant view:

```bash
streamlit run resto.py
```

Replace `resto.py` with `client.py`, `admin.py` or `coursier.py` to run the other modules.

## Running tests

Execute the test suite with [pytest](https://docs.pytest.org/):

```bash
pytest
```

At the moment the project does not contain tests, so `pytest` will report that no tests were found.

## Repository layout

```
admin.py       # admin interface
client.py      # customer order form
coursier.py    # courier dashboard
data.csv       # shared order storage
resto.py       # restaurant interface
requirements.txt  # Python dependencies
.devcontainer/    # configuration for development containers
```
