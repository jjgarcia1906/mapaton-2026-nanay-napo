"""
Componente de Filtros v2 - Dashboard Mapaton 2026
Sidebar con navegacion completa tipo menu web.
"""
import streamlit as st

ANOS = [2019, 2021, 2023, 2024, 2025]
CUENCAS = ["Todas", "Nanay", "Napo"]

def renderizar_filtros():
    st.sidebar.markdown("## Navegacion")

    st.sidebar.page_link("app.py", label="Inicio - Dashboard", icon="🏠")
    st.sidebar.page_link("pages/2_Problema.py", label="1. Problema", icon="🔍")
    st.sidebar.page_link("pages/3_Datos_y_Analisis.py", label="2. Datos y Analisis", icon="📊")
    st.sidebar.page_link("pages/4_Solucion.py", label="3. Solucion", icon="💡")
    st.sidebar.page_link("pages/5_Impacto.py", label="4. Impacto", icon="🎯")
    st.sidebar.page_link("pages/1_Flujo_de_Trabajo.py", label="Flujo de Trabajo GEE", icon="📋")

    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros")

    ano = st.sidebar.selectbox("Ano de analisis", ANOS, index=len(ANOS) - 1)
    cuenca = st.sidebar.selectbox("Subcuenca", CUENCAS, index=0)

    st.sidebar.markdown("---")

    if st.sidebar.button("🚨 REPORTA UNA AMENAZA", type="primary", use_container_width=True):
        st.switch_page("pages/6_Reporta_Amenaza.py")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**Grupo 03: Los Jaguares**\n\n"
        "Mapaton Regional 2026 - Iquitos\n\n"
        "*Cuencas Nanay y Napo*"
    )

    return {"ano": ano, "cuenca": cuenca}
