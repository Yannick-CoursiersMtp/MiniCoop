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
                "statut",
                "timestamp",
            ],
        )
        missions = commandes[commandes["coursier"] == nom]
        if missions.empty:
            st.info("Aucune livraison prévue.")
        else:
            for index, row in missions.iterrows():
                st.success(
                    f"{row['plat']} à livrer pour {row['nom']} à {row['adresse']} à {row['heure']}"
                )
                st.write(f"Statut actuel : {row['statut']}")
                if st.button("Confirmer la livraison", key=f"livree-{index}"):
                    commandes.at[index, 'statut'] = 'livrée'
                    commandes.to_csv("data.csv", index=False, header=False)
                    st.success("Commande livrée !")
    except FileNotFoundError:
        st.warning("Aucune commande trouvée.")
