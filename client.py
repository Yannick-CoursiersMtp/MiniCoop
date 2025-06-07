import streamlit as st
from orders import append_order

st.title("MiniCoop - Passer une commande")

nom = st.text_input("Nom du client")
adresse = st.text_input("Adresse de livraison")
restaurant = st.selectbox("Choisissez un restaurant", ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"])
plat = st.text_input("Plat commandé")
heure = st.time_input("Heure de livraison souhaitée")

if st.button("Envoyer la commande"):
    append_order(
        nom,
        adresse,
        restaurant,
        plat,
        heure.strftime("%H:%M"),
    )
    st.success("Commande envoyée avec succès !")
