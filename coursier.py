import streamlit as st
import pandas as pd

st.title("MiniCoop - Interface Coursier")

nom = st.text_input("Ton prénom (coursier)")

if nom:
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
        missions = commandes[commandes["coursier"] == nom]
        if missions.empty:
            st.info("Aucune livraison prévue.")
        else:
            for _, row in missions.iterrows():
                st.success(
                    f"{row['plat']} à livrer pour {row['nom']} "
                    f"à {row['adresse']} à {row['heure']}"
                )
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.warning("Aucune commande trouvée.")
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
