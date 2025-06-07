import streamlit as st
from datetime import datetime
from orders import append_order

st.title("MiniCoop - Passer une commande")

nom = st.text_input("Nom du client")
adresse = st.text_input("Adresse de livraison")
restaurant = st.selectbox("Choisissez un restaurant", ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"])
plat = st.text_input("Plat commandé")
heure = st.time_input("Heure de livraison souhaitée")

if st.button("Envoyer la commande"):
    nouvelle_commande = {
        "nom": nom,
        "adresse": adresse,
        "restaurant": restaurant,
        "plat": plat,
        "heure": heure.strftime("%H:%M"),
        "coursier": "",
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
    }
    append_order(nouvelle_commande)
    st.success("Commande envoyée avec succès !")
