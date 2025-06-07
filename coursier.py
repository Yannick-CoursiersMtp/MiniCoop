import streamlit as st
from orders import load_orders, update_status

st.title("MiniCoop - Interface Coursier")

nom = st.text_input("Ton prénom (coursier)")

if nom:
    commandes = load_orders()
    missions = commandes[commandes["coursier"] == nom]
    if missions.empty:
        st.info("Aucune livraison prévue.")
    else:
        for index, row in missions.iterrows():
            st.success(f"{row['plat']} à livrer pour {row['nom']} à {row['adresse']} à {row['heure']}")
            if st.button("Livrée", key=f"livree-{index}"):
                update_status(row['timestamp'], status="delivered")
                st.info("Commande marquée livrée")
