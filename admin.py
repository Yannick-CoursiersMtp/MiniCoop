import streamlit as st
import requests

st.title("MiniCoop - Interface Admin")

import os

if os.environ.get("STREAMLIT_SERVER_RUNNING"):
    resp = requests.get("http://localhost:8000/orders")
    if resp.ok:
        commandes = resp.json()
    else:
        st.warning("Aucune commande pour le moment.")
        commandes = []
else:
    commandes = []

for order in commandes:
    st.subheader(f"Commande de {order['nom']}")
    st.write(
        f"Plat : {order['plat']} | Resto : {order['restaurant']} | Heure : {order['heure']}"
    )
    st.write(f"Adresse : {order['adresse']}")
    coursier = st.text_input(
        "Affecter un coursier à cette commande :",
        value=order.get("coursier", ""),
        key=order["id"],
    )
    if st.button("Affecter", key=f"affecter-{order['id']}"):
        resp = requests.put(
            f"http://localhost:8000/orders/{order['id']}/assign",
            json={"coursier": coursier},
        )
        if resp.ok:
            st.success(f"{coursier} assigné à la commande.")
        else:
            st.error("Erreur lors de l'assignation")
