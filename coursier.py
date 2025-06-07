import streamlit as st
import requests


def main():
    st.title("MiniCoop - Interface Coursier")

    nom = st.text_input("Ton prénom (coursier)")

    API_URL = "http://localhost:8000"

    if nom:
        response = requests.get(f"{API_URL}/orders")
        commandes = response.json() if response.ok else []
        missions = [o for o in commandes if o["coursier"] == nom]
        if not missions:
            st.info("Aucune livraison prévue.")
        else:
            for row in missions:
                st.success(
                    f"{row['plat']} à livrer pour {row['nom']} "
                    f"à {row['adresse']} à {row['heure']}"
                )


if __name__ == "__main__":
    main()
