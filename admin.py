import streamlit as st
import pandas as pd
from orders import load_orders, assign_courier

st.title("MiniCoop - Interface Admin")

commandes = load_orders()
if commandes.empty:
    st.warning("Aucune commande pour le moment.")

for index, row in commandes.iterrows():
    st.subheader(f"Commande de {row['nom']}")
    st.write(f"Plat : {row['plat']} | Resto : {row['restaurant']} | Heure : {row['heure']}")
    st.write(f"Adresse : {row['adresse']}")
    coursier = st.text_input(
        f"Affecter un coursier à cette commande :", key=index
    )
    if st.button("Affecter", key=f"affecter-{index}"):
        assign_courier(index, coursier)
        st.success(f"{coursier} assigné à la commande.")
