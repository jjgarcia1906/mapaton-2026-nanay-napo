"""
DASHBOARD INTERACTIVO — Mapatón 2026
Grupo 03: Los Jaguares
Dinámica Fluvial y Minería Ilegal — Cuencas Nanay y Napo (2019–2025)

Ejecutar: streamlit run app.py
"""

import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Mapatón 2026 | Grupo 03: Los Jaguares",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PWA + Meta tags ---
st.markdown("""
<link rel="manifest" href="/app/static/manifest.json">
<meta name="theme-color" content="#003366">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="Alerta Mineria">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<script>
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/app/static/sw.js');
}
</script>
""", unsafe_allow_html=True)

# ─── Imports de componentes ───
from components.filtros import renderizar_filtros
from components.estadisticas import renderizar_kpis
from components.graficos import renderizar_graficos
from components.mapa import renderizar_mapa
from components.reportes import renderizar_panel_reporte
from components.metodologia import renderizar_metodologia
from utils.datos import cargar_datos, filtrar_datos

# ─── Carga de datos ───
@st.cache_data(ttl=3600)
def obtener_datos():
    return cargar_datos()

datos = obtener_datos()

# ═══════════════════════════════════════════════════════════════
# INTERFAZ DE USUARIO
# ═══════════════════════════════════════════════════════════════

# ─── Cabecera ───
col_titulo, col_logo = st.columns([5, 1])

with col_titulo:
    st.title("🌊 Dinámica Fluvial y Minería Ilegal")
    st.markdown(
        "**Análisis Multitemporal de Bancos de Arena en las Cuencas del Nanay y Napo (2019–2025)**  \n"
        "Grupo N° 03: **Los Jaguares** | Mapatón Regional 2026 — Fase Presencial Iquitos"
    )

with col_logo:
    st.markdown("🏆")
    st.caption("15–17 Julio 2026")

st.divider()

# --- Filtros (sidebar) ---
filtros = renderizar_filtros()

st.divider()

# --- Mapa GRANDE (full width) ---
draw_data = renderizar_mapa(ano=filtros["ano"], cuenca=filtros["cuenca"])

# --- Panel de Reporte Ciudadano ---
renderizar_panel_reporte(draw_data)

# --- KPIs ---
st.divider()
renderizar_kpis(
    datos["bancos"],
    datos["mineria"],
    ano=filtros["ano"],
    cuenca=filtros["cuenca"],
)

st.divider()

# --- Graficos ---
renderizar_graficos(
    datos["serie"],
    datos["correlacion"],
    ano=filtros["ano"],
    cuenca=filtros["cuenca"],
)

# --- Pie de pagina ---
st.divider()

# --- Metodologia ---
renderizar_metodologia()

st.divider()
st.markdown(
    "<small>Integrantes: Garcia Del Aguila Jordi Jairo | Torres Lopez C. Jessenia "
    "| Paima Roque Rody | Murayari Ortiz Rey Judan</small>",
    unsafe_allow_html=True,
)
