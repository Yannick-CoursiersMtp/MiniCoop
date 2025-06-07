import streamlit as st
import requests
import os

st.title("MiniCoop - Interface Restaurant")

nom_resto = st.selectbox(
    "Choisissez votre restaurant",
    ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"],
)

if os.environ.get("STREAMLIT_SERVER_RUNNING"):
    resp = requests.get("http://localhost:8000/orders")
    if resp.ok:
        commandes = [c for c in resp.json() if c["restaurant"] == nom_resto]
    else:
        commandes = []
else:
    commandes = []

if not commandes:
    st.info("Aucune commande en attente.")
else:
    for order in commandes:
        st.subheader(f"Commande de {order['nom']}")
        st.write(
            f"Plat : {order['plat']} | Adresse : {order['adresse']} | Heure : {order['heure']}"
        )
        st.write(
            "Coursier assigné : "
            f"{order['coursier'] if order['coursier'] else 'Pas encore'}"
        )
        if st.button("Commande prête", key=f"prête-{order['id']}"):
            requests.put(f"http://localhost:8000/orders/{order['id']}/ready")
