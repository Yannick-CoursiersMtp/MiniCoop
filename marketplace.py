import json
from datetime import datetime
import pandas as pd
import streamlit as st

st.title("MiniCoop - Place de marché")

# Charger la liste des restaurants et leurs menus
try:
    with open("restaurants.json", "r", encoding="utf-8") as f:
        menus = json.load(f)
except FileNotFoundError:
    st.error("Fichier restaurants.json introuvable")
    st.stop()

restaurants = list(menus.keys())
choix_resto = st.selectbox("Choisissez un restaurant", restaurants)

if choix_resto:
    st.subheader("Menu")
    plats = menus[choix_resto]
    plat = st.selectbox("Choisissez un plat", plats)

    st.subheader("Passer la commande")
    nom = st.text_input("Nom du client")
    adresse = st.text_input("Adresse de livraison")
    heure = st.time_input("Heure de livraison souhaitée")

    if st.button("Commander"):
        nouvelle_commande = pd.DataFrame([{"nom": nom,
                                            "adresse": adresse,
                                            "restaurant": choix_resto,
                                            "plat": plat,
                                            "heure": heure.strftime("%H:%M"),
                                            "coursier": "",
                                            "timestamp": datetime.now().isoformat()}])
        nouvelle_commande.to_csv("data.csv", mode="a", header=False, index=False)
        st.success("Commande envoyée !")

