import streamlit as st
from datetime import datetime
import json
import requests
import websocket
import threading

st.set_page_config(
    page_title="MiniCoop - Passer une commande",
    page_icon="🍽️",
    layout="centered",
)

st.markdown(
    """
    <style>
        body {
            background-color: #f5f5f5;
        }
        .form-container {
            background-color: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            height: 3em;
            width: 100%;
            border-radius: 4px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with open("menus.json", "r") as f:
    menus = json.load(f)

st.markdown("<h1 style='text-align:center;color:#ff4b4b;'>MiniCoop</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    nom = st.text_input("Nom du client")
    adresse = st.text_input("Adresse de livraison")
    restaurant = st.selectbox("Choisissez un restaurant", list(menus.keys()))
    plat = st.selectbox("Plat commandé", menus[restaurant])
    heure = st.time_input("Heure de livraison souhaitée")
    envoyer = st.button("Envoyer la commande", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

if envoyer:
    resp = requests.post(
        "http://localhost:8000/orders",
        json={
            "nom": nom,
            "adresse": adresse,
            "restaurant": restaurant,
            "plat": plat,
            "heure": heure.strftime("%H:%M"),
        },
    )
    if resp.ok:
        data = resp.json()
        order_id = data["id"]
        st.success("Commande envoyée avec succès !")

        status = st.empty()

        def listen():
            ws = websocket.create_connection(f"ws://localhost:8000/ws/orders/{order_id}")
            while True:
                msg = ws.recv()
                event = json.loads(msg)
                if event.get("event") == "assigned":
                    status.info(f"Coursier assigné : {event['courier']}")
                elif event.get("event") == "ready":
                    status.success("Votre commande est prête !")
                    break

        threading.Thread(target=listen, daemon=True).start()
    else:
        st.error("Erreur lors de l'envoi de la commande")
