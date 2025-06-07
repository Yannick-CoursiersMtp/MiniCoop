# MiniCoop

MiniCoop is a simple demo of a food delivery workflow built with [Streamlit](https://streamlit.io/). It is composed of a few small applications for different actors in the delivery process:

- **Client** (`client.py`) – form for customers to place an order.
- **Restaurant** (`resto.py`) – view pending orders for a given restaurant.
- **Admin** (`admin.py`) – assign a courier to each order.
- **Courrier** (`coursier.py`) – see the deliveries assigned to a given courier.

Orders are stored in a CSV file named `data.csv`. The file is listed in `.gitignore` so that example orders are not committed to the repository. Each component of the workflow reads or writes to this file. The interfaces are meant for local demonstrations, so there is no authentication or persistence beyond the CSV file.

## Running locally

Make sure `streamlit` is installed and run any of the interfaces. For example to launch the restaurant view:

```bash
streamlit run resto.py
```

Open the provided local URL in your browser and interact with the app.

## Repository layout

```
admin.py   # admin interface
client.py  # customer order form
coursier.py  # courier dashboard
resto.py   # restaurant interface
data.csv   # shared order storage
.devcontainer/devcontainer.json  # configuration for Codespaces/devcontainers
```

## Development container

The project includes a devcontainer configuration. When used inside GitHub Codespaces or a compatible environment it installs dependencies and automatically launches `resto.py`.

The devcontainer provides a ready-to-use development environment. It sets up Python 3 with all required packages and starts the restaurant interface as soon as the container is attached, letting you test the application without manual setup.


## FastAPI backend

A small API built with FastAPI is available under `backend/`. It stores orders in a SQLite database and exposes a few endpoints:

- `POST /orders` — create a new order.
- `GET /orders` — list all orders.
- `PUT /orders/{id}/assign` — assign a courier to an order.
- `POST /payments` — register a payment for an order.

Run it locally with:

```bash
uvicorn backend.main:app --reload
```
