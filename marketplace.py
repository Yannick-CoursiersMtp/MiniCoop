import streamlit as st
import json

st.title("MiniCoop - Marketplace")

with open("menus.json", "r") as f:
    menus = json.load(f)

for resto, plats in menus.items():
    st.header(resto)
    for plat in plats:
        st.write(f"- {plat}")
