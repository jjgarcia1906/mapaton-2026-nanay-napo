"""
Componente de Estadisticas v2 - Dashboard Mapaton 2026
KPIs con descripcion para cualquier persona
"""
import streamlit as st
import pandas as pd

def renderizar_kpis(df_bancos, df_mineria, ano=None, cuenca=None):
    # Filtrar por año
    b = df_bancos.copy()
    m = df_mineria.copy()

    if ano and "ano" in b.columns:
        b = b[b["ano"] == int(ano)]
    if ano and "ano" in m.columns:
        m = m[m["ano"] == int(ano)]

    # Filtrar por cuenca (si hay datos desagregados)
    if cuenca and cuenca != "Todas" and "cuenca" in b.columns:
        b_c = b[b["cuenca"].str.upper() == cuenca.upper()]
        if len(b_c) > 0:
            b = b_c
    if cuenca and cuenca != "Todas" and "cuenca" in m.columns:
        m_c = m[m["cuenca"].str.upper() == cuenca.upper()]
        if len(m_c) > 0:
            m = m_c

    area_arena = b["area_ha"].sum() if not b.empty and "area_ha" in b.columns else 0
    area_mineria = m["area_ha"].sum() if not m.empty and "area_ha" in m.columns else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏖️ Bancos de Arena", f"{area_arena:,.0f} ha",
                  help="Superficie total de playas y bancos de arena detectados en las imagenes satelitales. "
                       "Un valor alto indica mayor exposicion de arena durante la vaciante.")

    with col2:
        st.metric("⛏️ Mineria Detectada", f"{area_mineria:,.0f} ha",
                  help="Area total clasificada como mineria aurifera (piscinas de decantacion, zonas dragadas y "
                       "agua turbia por sedimentos). Detectado mediante analisis espectral de imagenes Sentinel-2.")

    with col3:
        pct_mineria = (area_mineria / area_arena * 100) if area_arena > 0 else 0
        st.metric("📊 Mineria vs Arena", f"{pct_mineria:.1f}%",
                  help="Relacion porcentual entre el area minera y el area de bancos de arena. "
                       "Un porcentaje alto sugiere fuerte presion minera sobre el ecosistema fluvial.")

    with col4:
        nombre = cuenca if cuenca != "Todas" else "Ambas cuencas"
        st.metric("🌊 Subcuenca", nombre,
                  help="Subcuenca analizada: Nanay (alta cuenca) o Napo (media cuenca).")

    st.caption("💡 **Como interpretar:** Los bancos de arena son playas naturales que emergen en epoca de vaciante "
               "(agos-nov). La mineria aurifera ilegal usa dragas que remueven el lecho del rio, destruyendo estas "
               "playas y contaminando el agua con sedimentos y mercurio. Compara los valores entre años para ver "
               "la tendencia.")

    # Nota especial para Nanay
    if cuenca == "Nanay" and area_arena < 50:
        st.info("⚠️ **Caso Nanay:** El rio Nanay tiene muy poca arena expuesta (cauce angosto, "
                "alta cobertura vegetal en las orillas). Los valores de 'Mineria vs Arena' pueden superar "
                "el 100% porque hay mas area minera detectada que arena. Esto NO es un error: refleja "
                "que la mineria esta ocurriendo principalmente en tierra firme (orillas y zonas de bosque "
                "talado), no en el cauce. La arena del Nanay casi ha desaparecido.")
