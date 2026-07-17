"""
Pagina: Reporta una Amenaza v3 - Dashboard Mapaton 2026
Mapa interactivo + formulario con auto-relleno al hacer clic.
"""
import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from pyproj import Transformer
import json, os, datetime

st.set_page_config(page_title="Reporta una Amenaza | Mapaton 2026", page_icon="🚨", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORTES_FILE = os.path.join(DATA_DIR, "reportes_ciudadanos.json")

t_wgs84_utm = Transformer.from_crs("EPSG:4326", "EPSG:32718", always_xy=True)

def cargar_reportes():
    if os.path.isfile(REPORTES_FILE):
        with open(REPORTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_reporte(datos):
    reportes = cargar_reportes()
    datos["id"] = len(reportes) + 1
    datos["fecha"] = datetime.datetime.now().isoformat()
    reportes.append(datos)
    with open(REPORTES_FILE, "w", encoding="utf-8") as f:
        json.dump(reportes, f, ensure_ascii=False, indent=2)
    return datos["id"]

# Inicializar
for k, v in [("reporte_este", 0.0), ("reporte_norte", 0.0), ("reporte_lat", 0.0),
             ("reporte_lon", 0.0), ("punto_colocado", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

st.title("🚨 Reporta una Amenaza Minera")
st.markdown("Haz clic en el mapa sobre la ubicacion de la draga o mineria que quieres reportar.")

# --- MAPA ---
col_mapa, col_form = st.columns([3, 2])

with col_mapa:
    st.markdown("### 📍 Selecciona la ubicacion")

    lat_c = st.session_state.reporte_lat if st.session_state.punto_colocado else -3.5
    lon_c = st.session_state.reporte_lon if st.session_state.punto_colocado else -73.5

    m = folium.Map(location=[lat_c, lon_c], zoom_start=14 if st.session_state.punto_colocado else 9,
                   tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                   attr="Esri", control_scale=True)

    if st.session_state.punto_colocado:
        folium.Marker(
            [st.session_state.reporte_lat, st.session_state.reporte_lon],
            popup="Ubicacion seleccionada",
            icon=folium.Icon(color="red", icon="crosshairs", prefix="fa"),
        ).add_to(m)

    Draw(
        export=False, position="topleft",
        draw_options={
            "polyline": False, "rectangle": False, "circle": False,
            "circlemarker": False,
            "polygon": {"allowIntersection": False, "showArea": True, "shapeOptions": {"color": "#FF0000"}},
            "marker": {},
        },
        edit_options={"edit": True, "remove": True},
    ).add_to(m)

    # Boton de geolocalizacion
    st.markdown("""
    <button onclick="getLocation()" style="background:#003366;color:white;border:none;
    padding:6px 12px;border-radius:4px;cursor:pointer;margin-top:5px;font-size:14px;">
    📍 Usar mi ubicacion actual</button>
    <script>
    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                window.location.href = window.location.pathname + '?lat=' + lat + '&lon=' + lon;
            }, function(err) {
                alert('No se pudo obtener tu ubicacion. Permite el acceso a GPS en tu navegador.');
            });
        } else {
            alert('Tu navegador no soporta geolocalizacion.');
        }
    }
    </script>
    """, unsafe_allow_html=True)

    resultado = st_folium(m, width=None, height=500, returned_objects=["last_active_drawing"])

    # Si vienen coordenadas por URL (geolocalizacion)
    query = st.query_params
    if "lat" in query and "lon" in query:
        try:
            lat_u = float(query["lat"]); lon_u = float(query["lon"])
            e, n = t_wgs84_utm.transform(lon_u, lat_u)
            st.session_state.reporte_este = round(e, 1)
            st.session_state.reporte_norte = round(n, 1)
            st.session_state.reporte_lat = round(lat_u, 6)
            st.session_state.reporte_lon = round(lon_u, 6)
            st.session_state.punto_colocado = True
        except:
            pass

    if resultado and resultado.get("last_active_drawing"):
        dibujo = resultado["last_active_drawing"]
        geo = dibujo.get("geometry", {})
        coords = geo.get("coordinates", [])
        if coords and len(coords) >= 2:
            lon, lat = coords[0], coords[1]
            este, norte = t_wgs84_utm.transform(lon, lat)
            st.session_state.reporte_este = round(este, 1)
            st.session_state.reporte_norte = round(norte, 1)
            st.session_state.reporte_lat = round(lat, 6)
            st.session_state.reporte_lon = round(lon, 6)
            st.session_state.punto_colocado = True
            st.rerun()

    if st.session_state.punto_colocado:
        if st.button("🗑️ Borrar punto", type="secondary"):
            for k in ["punto_colocado", "reporte_este", "reporte_norte", "reporte_lat", "reporte_lon"]:
                st.session_state[k] = 0.0 if k != "punto_colocado" else False
            st.rerun()

# --- FORMULARIO (sin st.form, inputs directos) ---
with col_form:
    st.markdown("### 📝 Detalles del reporte")
    st.caption("Coordenadas UTM (Zona 18 Sur)")

    c1, c2 = st.columns(2)
    with c1:
        este = st.number_input("Este (X)", key="ui_este", value=st.session_state.reporte_este, step=1.0)
    with c2:
        norte = st.number_input("Norte (Y)", key="ui_norte", value=st.session_state.reporte_norte, step=1.0)

    if st.session_state.punto_colocado:
        st.success(f"📍 Capturado: {st.session_state.reporte_lat:.6f}, {st.session_state.reporte_lon:.6f}")

    tipo = st.selectbox("Tipo de amenaza", [
        "Draga activa en el rio", "Campamento minero en la orilla",
        "Piscina de decantacion", "Suelo removido / deforestacion",
        "Agua turbia por actividad minera", "Maquinaria pesada",
        "Otra evidencia de mineria ilegal"
    ])

    descripcion = st.text_area("Describe lo que observaste",
        placeholder="Cuantas dragas, fecha aproximada, personas trabajando...", height=100)

    fecha_obs = st.date_input("Fecha aproximada")

    c3, c4 = st.columns(2)
    with c3:
        nombre = st.text_input("Tu nombre (opcional)")
    with c4:
        contacto = st.text_input("Telefono o correo (opcional)")

    if st.button("🚨 ENVIAR REPORTE", type="primary", use_container_width=True):
        if este == 0.0 and norte == 0.0:
            st.error("Selecciona un punto en el mapa o ingresa coordenadas manualmente.")
        elif not descripcion.strip():
            st.error("Describe lo que observaste.")
        else:
            r = {
                "tipo": tipo, "descripcion": descripcion,
                "contacto": f"{nombre} - {contacto}" if nombre or contacto else "Anonimo",
                "latitud": st.session_state.reporte_lat if st.session_state.punto_colocado else 0,
                "longitud": st.session_state.reporte_lon if st.session_state.punto_colocado else 0,
                "utm_este": este, "utm_norte": norte, "utm_zona": "18S",
                "fecha_observacion": str(fecha_obs),
            }
            rid = guardar_reporte(r)
            st.success(f"✅ Reporte #{rid} enviado.")
            st.balloons()
            for k in ["punto_colocado", "reporte_este", "reporte_norte", "reporte_lat", "reporte_lon"]:
                st.session_state[k] = 0.0 if k != "punto_colocado" else False

# Historial
st.divider()
with st.expander(f"📋 Reportes anteriores ({len(cargar_reportes())} registros)"):
    reportes = cargar_reportes()
    for r in reversed(reportes[-20:]):
        st.markdown(f"**#{r['id']}** - {r.get('fecha','')[:10]} - {r.get('tipo','')}")
        st.caption(f"UTM: {r.get('utm_este','')}, {r.get('utm_norte','')}")
        st.divider()
