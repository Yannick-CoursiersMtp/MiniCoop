import streamlit as st
from orders import load_orders, update_status

st.title("MiniCoop - Interface Admin")

commandes = load_orders()
if commandes.empty:
    st.warning("Aucune commande pour le moment.")

for index, row in commandes.iterrows():
    st.subheader(f"Commande de {row['nom']}")
    st.write(f"Plat : {row['plat']} | Resto : {row['restaurant']} | Heure : {row['heure']}")
    st.write(f"Adresse : {row['adresse']}")
    coursier = st.text_input("Affecter un coursier ", key=index)
    if st.button("Affecter", key=f"affecter-{index}"):
        update_status(row['timestamp'], coursier=coursier)
        st.success(f"{coursier} assigné à la commande.")
