import streamlit as st
import pandas as pd
from datetime import datetime
import json

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
