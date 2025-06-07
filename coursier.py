import streamlit as st
import requests
import os

st.title("MiniCoop - Interface Coursier")

nom = st.text_input("Ton prénom (coursier)")

if nom and os.environ.get("STREAMLIT_SERVER_RUNNING"):
    resp = requests.get("http://localhost:8000/orders")
    if resp.ok:
        commandes = [c for c in resp.json() if c["coursier"] == nom]
    else:
        commandes = []

    if not commandes:
        st.info("Aucune livraison prévue.")
    else:
        for order in commandes:
            st.success(
                f"{order['plat']} à livrer pour {order['nom']} "
                f"à {order['adresse']} à {order['heure']}"
            )
