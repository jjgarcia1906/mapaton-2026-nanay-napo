"""
Componente de Mapa v5 - Dashboard Mapaton 2026
Mapa grande + plugin Draw para reportes ciudadanos.
"""
import streamlit as st
import folium
from folium.plugins import Draw, Fullscreen
from streamlit_folium import st_folium
import json, os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MAPAS_DIR = os.path.join(DATA_DIR, "mapas_base")
AOI_GEOJSON = os.path.join(DATA_DIR, "aoi_nanay_napo.geojson")

BOUNDS = {
    2019: [[-3.919, -74.814], [-2.458, -73.089]],
    2021: [[-3.919, -74.814], [-2.458, -73.089]],
    2023: [[-3.919, -74.814], [-2.458, -73.089]],
    2024: [[-3.919, -74.814], [-2.458, -73.089]],
    2025: [[-3.919, -74.814], [-2.458, -73.089]],
}
COLORES_ANIO = {2019: 'purple', 2021: 'blue', 2023: 'green', 2024: 'orange', 2025: 'red'}

def renderizar_mapa(ano=None, cuenca=None):
    st.subheader("Mapa Interactivo - Cuencas Nanay y Napo")
    st.caption("Usa las herramientas de dibujo (barra izquierda del mapa) para reportar dragas o mineria.")

    anio = ano if ano else 2025

    m = folium.Map(location=[-3.5, -73.5], zoom_start=9,
                   tiles="OpenStreetMap", control_scale=True)

    # Pantalla completa
    Fullscreen().add_to(m)

    # Satelite
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satelite (fondo)",
    ).add_to(m)

    # RGB todos los anos
    for a in [2019, 2021, 2023, 2024, 2025]:
        png = os.path.join(MAPAS_DIR, f"RGB_{a}_Base.png")
        if os.path.isfile(png) and a in BOUNDS:
            b = BOUNDS[a]
            folium.raster_layers.ImageOverlay(
                image=png, bounds=[b[0], b[1]], opacity=0.90,
                name=f"Satelite RGB {a}", show=(a == anio),
            ).add_to(m)

    # AOI
    if os.path.isfile(AOI_GEOJSON):
        with open(AOI_GEOJSON, "r", encoding="utf-8") as f:
            aoi_data = json.load(f)
        if aoi_data.get("features") and len(aoi_data["features"]) > 0:
            simple = {"type": "FeatureCollection", "features": [aoi_data["features"][0]]}
            folium.GeoJson(
                simple, name="Area de Estudio (AOI)",
                style_function=lambda x: {
                    "fillColor": "#003366", "fillOpacity": 0.08,
                    "color": "#003366", "weight": 2.5,
                },
            ).add_to(m)

    # Arena
    geojson_arena = os.path.join(DATA_DIR, f"arena_{anio}.geojson")
    if os.path.isfile(geojson_arena):
        try:
            with open(geojson_arena, "r", encoding="utf-8") as f:
                arena_data = json.load(f)
            folium.GeoJson(
                arena_data, name=f"Arena {anio}",
                style_function=lambda x: {
                    "fillColor": "#FFD700", "color": "#DAA520",
                    "weight": 1, "fillOpacity": 0.6,
                },
            ).add_to(m)
        except:
            pass

    # Mineria
    geojson_min = os.path.join(DATA_DIR, f"mineria_{anio}.geojson")
    if not os.path.isfile(geojson_min):
        geojson_min = os.path.join(DATA_DIR, f"Mineria_Vector_{anio}.geojson")
    if os.path.isfile(geojson_min):
        try:
            with open(geojson_min, "r", encoding="utf-8") as f:
                min_data = json.load(f)
            color = COLORES_ANIO.get(anio, 'red')
            folium.GeoJson(
                min_data, name=f"Mineria {anio}",
                style_function=lambda x, c=color: {
                    "fillColor": c, "color": c, "weight": 1, "fillOpacity": 0.5,
                },
            ).add_to(m)
        except:
            pass

    # Marcadores referencia
    folium.Marker([-3.75, -73.30], popup="<b>Rio Nanay</b>",
                  icon=folium.Icon(color="blue", icon="water", prefix="fa")).add_to(m)
    folium.Marker([-3.10, -73.20], popup="<b>Rio Napo</b>",
                  icon=folium.Icon(color="green", icon="water", prefix="fa")).add_to(m)

    # Plugin de dibujo para reportes
    Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "circlemarker": False,
            "polygon": {"allowIntersection": False, "showArea": True, "shapeOptions": {"color": "#FF0000"}},
            "marker": True,
        },
        edit_options={"edit": False, "remove": True},
    ).add_to(m)

    folium.LayerControl().add_to(m)

    # Mapa GRANDE
    resultado = st_folium(m, width=1100, height=700, returned_objects=["last_active_drawing", "all_drawings"])

    return resultado
