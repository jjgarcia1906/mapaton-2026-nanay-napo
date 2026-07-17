"""
Componente de Reporte Ciudadano - Dashboard Mapaton 2026
Permite dibujar en el mapa y reportar dragas/mineria.
"""
import streamlit as st
import json, os, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORTES_FILE = os.path.join(DATA_DIR, "reportes_ciudadanos.json")

def cargar_reportes():
    if os.path.isfile(REPORTES_FILE):
        with open(REPORTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_reporte(tipo, descripcion, contacto, lat, lon, coords_raw):
    reportes = cargar_reportes()
    reporte = {
        "id": len(reportes) + 1,
        "fecha": datetime.datetime.now().isoformat(),
        "tipo": tipo,
        "descripcion": descripcion,
        "contacto": contacto,
        "latitud": lat,
        "longitud": lon,
        "coordenadas_raw": coords_raw,
    }
    reportes.append(reporte)
    with open(REPORTES_FILE, "w", encoding="utf-8") as f:
        json.dump(reportes, f, ensure_ascii=False, indent=2)
    return reporte

def renderizar_panel_reporte(datos_mapa=None):
    """
    Muestra panel de reporte si el usuario dibujo algo en el mapa.
    datos_mapa: dict con 'last_active_drawing', 'all_drawings', etc. de st_folium
    """
    if datos_mapa is None:
        return

    dibujo = datos_mapa.get("last_active_drawing")
    if dibujo is None:
        return

    st.divider()
    st.markdown("### 🚨 Reporte de Actividad Minera Ilegal")

    # Extraer coordenadas del dibujo
    geo = dibujo.get("geometry", {})
    coords = []
    tipo_geo = geo.get("type", "")

    if tipo_geo == "Point":
        coords = geo.get("coordinates", [])
    elif tipo_geo == "Polygon":
        coords = geo.get("coordinates", [[0, 0]])[0]

    if coords and len(coords) >= 2:
        lon, lat = coords[0], coords[1]
    else:
        st.warning("No se pudo obtener coordenadas del dibujo.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latitud", f"{lat:.6f}")
    with col2:
        st.metric("Longitud", f"{lon:.6f}")

    tipo = st.selectbox("Tipo de observacion", [
        "Draga activa", "Campamento minero", "Piscina de decantacion",
        "Suelo removido", "Agua turbia", "Otra evidencia de mineria"
    ])

    descripcion = st.text_area("Descripcion de lo observado",
        placeholder="Describe que viste, cuantas dragas, fecha aproximada...")

    contacto = st.text_input("Tu nombre o correo (opcional)",
        placeholder="Para seguimiento del reporte")

    enviado = st.button("Enviar Reporte", type="primary")

    if enviado:
        if not descripcion.strip():
            st.error("Por favor describe lo que observaste.")
        else:
            reporte = guardar_reporte(tipo, descripcion, contacto, lat, lon, coords)
            st.success(f"Reporte #{reporte['id']} enviado correctamente.")
            st.info("El administrador sera notificado. Gracias por contribuir a la vigilancia de nuestros rios.")
            st.balloons()

    # Mostrar reportes recientes
    with st.expander(f"Ver reportes anteriores ({len(cargar_reportes())} registros)"):
        reportes = cargar_reportes()
        if reportes:
            for r in reversed(reportes[-10:]):
                st.markdown(f"**#{r['id']}** - {r['fecha'][:10]} - {r['tipo']}")
                st.caption(f"📍 {r['latitud']:.4f}, {r['longitud']:.4f} | {r['descripcion'][:80]}...")
                st.divider()
        else:
            st.caption("No hay reportes todavia.")
