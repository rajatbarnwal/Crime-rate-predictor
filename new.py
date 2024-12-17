import streamlit as st
import subprocess
import sys
import folium

st.write("just try")
g, u = st.columns(2)

if g.button("info"):
    subprocess.run(["streamlit","run","main.py"])

