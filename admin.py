import streamlit as st
import requests


def main():
    st.title("MiniCoop - Interface Admin")

    API_URL = "http://localhost:8000"

    response = requests.get(f"{API_URL}/orders")
    if not response.ok:
        st.warning("Aucune commande pour le moment.")
        commandes = []
    else:
        commandes = response.json()

    for row in commandes:
        st.subheader(f"Commande de {row['nom']}")
        st.write(
            f"Plat : {row['plat']} | Resto : {row['restaurant']} | "
            f"Heure : {row['heure']}"
        )
        st.write(f"Adresse : {row['adresse']}")
        coursier = st.text_input(
            "Affecter un coursier à cette commande :",
            value=row["coursier"],
            key=row["id"],
        )
        if st.button("Affecter", key=f"affecter-{row['id']}"):
            requests.put(
                f"{API_URL}/orders/{row['id']}/assign",
                json={"coursier": coursier},
            )
            st.session_state[row["id"]] = coursier
            st.success(f"{coursier} assigné à la commande.")


if __name__ == "__main__":
    main()
