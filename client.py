import streamlit as st
import pandas as pd
from datetime import datetime

st.title("MiniCoop - Passer une commande")

nom = st.text_input("Nom du client")
adresse = st.text_input("Adresse de livraison")
restaurant = st.selectbox("Choisissez un restaurant", ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"])
plat = st.text_input("Plat commandé")
heure = st.time_input("Heure de livraison souhaitée")

if st.button("Envoyer la commande"):
    nouvelle_commande = pd.DataFrame([
        {
            "nom": nom,
            "adresse": adresse,
            "restaurant": restaurant,
            "plat": plat,
            "heure": heure.strftime("%H:%M"),
            "coursier": "",
            "statut": "en_attente",
            "timestamp": datetime.now().isoformat(),
        }
    ])
    nouvelle_commande.to_csv("data.csv", mode="a", header=False, index=False)
    st.success("Commande envoyée avec succès !")
