"""
Página: Flujo de Trabajo — Dashboard Mapatón 2026
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Flujo GEE — Mapatón 2026",
    page_icon="📋",
    layout="wide",
)

st.title("📋 Flujo de Trabajo — Google Earth Engine")

st.markdown("""
Esta página muestra la secuencia completa de scripts necesarios para procesar
los datos satelitales, desde la subida de shapes hasta el dashboard final.
""")

# Cargar el HTML del flujo
html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "flujo_trabajo.html")

try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=1300, scrolling=True)
except FileNotFoundError:
    st.warning("Archivo flujo_trabajo.html no encontrado en assets/")
    st.info("Copialo desde la carpeta raíz del proyecto.")
