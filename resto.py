import streamlit as st
import requests


def main():
    st.title("MiniCoop - Interface Restaurant")

    nom_resto = st.selectbox(
        "Choisissez votre restaurant",
        ["Pizza MTP", "Tacos Deluxe", "Vegan Bowl"],
    )

    API_URL = "http://localhost:8000"

    response = requests.get(f"{API_URL}/orders")
    commandes = response.json() if response.ok else []
    commandes_resto = [c for c in commandes if c["restaurant"] == nom_resto]

    if not commandes_resto:
        st.info("Aucune commande en attente.")
    else:
        for index, row in enumerate(commandes_resto):
            st.subheader(f"Commande de {row['nom']}")
            st.write(
                f"Plat : {row['plat']} | Adresse : {row['adresse']} | "
                f"Heure : {row['heure']}"
            )
            st.write(
                "Coursier assigné : "
                f"{row['coursier'] if row['coursier'] else 'Pas encore'}"
            )
            st.button(
                "Commande prête",
                key=f"prête-{index}",
            )  # (action pas encore enregistrée)


if __name__ == "__main__":
    main()
