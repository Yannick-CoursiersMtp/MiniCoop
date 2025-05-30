import streamlit as st
import pandas as pd

st.title("MiniCoop - Interface Restaurant")

nom_resto = st.selectbox("Choisissez votre restaurant", ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"])

try:
    commandes = pd.read_csv("data.csv", names=["nom", "adresse", "restaurant", "plat", "heure", "coursier", "timestamp"])
    commandes_resto = commandes[commandes["restaurant"] == nom_resto]

    if commandes_resto.empty:
        st.info("Aucune commande en attente.")
    else:
        for index, row in commandes_resto.iterrows():
            st.subheader(f"Commande de {row['nom']}")
            st.write(f"Plat : {row['plat']} | Adresse : {row['adresse']} | Heure : {row['heure']}")
            st.write(f"Coursier assigné : {row['coursier'] if row['coursier'] else 'Pas encore'}")
            st.button("Commande prête", key=f"prête-{index}")  # (action pas encore enregistrée)

except FileNotFoundError:
    st.warning("Aucune commande disponible.")
