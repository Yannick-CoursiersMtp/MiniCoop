import streamlit as st
from orders import orders_for_courier

st.title("MiniCoop - Interface Coursier")

nom = st.text_input("Ton prénom (coursier)")

if nom:
    missions = orders_for_courier(nom)
    if missions.empty:
        st.info("Aucune livraison prévue.")
    else:
        for _, row in missions.iterrows():
            st.success(
                f"{row['plat']} à livrer pour {row['nom']} à {row['adresse']} à {row['heure']}"
            )
