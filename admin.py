import streamlit as st
import pandas as pd

st.title("MiniCoop - Interface Admin")

try:
    commandes = pd.read_csv(
        "data.csv",
        names=[
            "nom",
            "adresse",
            "restaurant",
            "plat",
            "heure",
            "coursier",
            "timestamp",
        ],
    )
except (FileNotFoundError, pd.errors.EmptyDataError):
    st.warning("Aucune commande pour le moment.")
    commandes = pd.DataFrame(
        columns=[
            "nom",
            "adresse",
            "restaurant",
            "plat",
            "heure",
            "coursier",
            "timestamp",
        ]
    )

for index, row in commandes.iterrows():
    st.subheader(f"Commande de {row['nom']}")
    st.write(
        f"Plat : {row['plat']} | Resto : {row['restaurant']} | "
        f"Heure : {row['heure']}"
    )
    st.write(f"Adresse : {row['adresse']}")
    coursier = st.text_input(
        "Affecter un coursier à cette commande :",
        value=row["coursier"],
        key=index,
    )
    if st.button("Affecter", key=f"affecter-{index}"):
        commandes.at[index, "coursier"] = coursier
        commandes.to_csv("data.csv", index=False, header=False)
        st.session_state[index] = coursier
        st.success(f"{coursier} assigné à la commande.")
