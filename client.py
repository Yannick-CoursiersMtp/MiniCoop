import streamlit as st
import pandas as pd
from datetime import datetime
import json

with open("menus.json", "r") as f:
    menus = json.load(f)

st.title("MiniCoop - Passer une commande")

nom = st.text_input("Nom du client")
adresse = st.text_input("Adresse de livraison")
restaurant = st.selectbox("Choisissez un restaurant", list(menus.keys()))
plat = st.selectbox("Plat commandé", menus[restaurant])
heure = st.time_input("Heure de livraison souhaitée")

if st.button("Envoyer la commande"):
    nouvelle_commande = pd.DataFrame([{
        "nom": nom,
        "adresse": adresse,
        "restaurant": restaurant,
        "plat": plat,
        "heure": heure.strftime("%H:%M"),
        "coursier": "",
        "timestamp": datetime.now().isoformat()
    }])
    nouvelle_commande.to_csv("data.csv", mode="a", header=False, index=False)
    st.success("Commande envoyée avec succès !")
