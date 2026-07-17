"""
Pagina: Datos y Analisis - Dashboard Mapaton 2026
"""
import streamlit as st

st.set_page_config(page_title="Datos y Analisis | Mapaton 2026", page_icon="📊", layout="wide")

st.title("2. Datos y Analisis")

tab1, tab2, tab3 = st.tabs(["Fuentes de Datos", "Metodologia", "Implementacion GEE"])

with tab1:
    st.markdown("""
### 2.1. Area de Estudio (AOI)

| Parametro | Especificacion |
|-----------|----------------|
| Ubicacion | Provincia de Maynas, departamento de Loreto, Peru |
| Subcuencas | Nanay (alta cuenca) y Napo (media cuenca) |
| CRS de trabajo | EPSG:32718 - WGS84 / UTM Zona 18 Sur |
| Extension aproximada | ~15,000 km2 (area combinada de ambas subcuencas) |

### 2.2. Fuentes de Datos

| Tipo de dato | Fuente | Resolucion / Detalle | Uso en el estudio |
|--------------|--------|---------------------|-------------------|
| Optica multiespectral | Sentinel-2 (ESA) | 10 m (B2, B3, B4, B8), 20 m (SWIR) | Clasificacion de cobertura, NDVI, NDWI, MNDWI |
| Radar (SAR) | Sentinel-1 (ESA) | 10 m, banda C (VV, VH) | Deteccion en epoca de creciente/nubes |
| Cartografia vectorial | GOREL, MINAM, SERNANP | Escalas 1:100,000-1:250,000 | Red hidrografica, ANP, limites comunales |
| Alertas de deforestacion | GEOBOSQUES (MINAM) | Alertas mensuales (30 m) | Validacion espacial de eventos de deforestacion |
| Hidrologia | GOREL / SENAMHI | Estaciones hidrometricas | Delimitacion de epocas de vaciante vs. creciente |

### 2.3. Ventanas Temporales

Periodos de vaciante (agosto-noviembre) para los años 2019, 2021, 2023, 2024 y 2025, con filtro de cobertura de nubes < 20%.
""")

with tab2:
    st.markdown("""
### 3. Analisis - Fases de Procesamiento

#### Fase 1: Preparacion de Datos
1. Descarga y filtrado de imagenes Sentinel-2 Level-2A para cada periodo de vaciante
2. Descarga complementaria de imagenes Sentinel-1 GRD como respaldo
3. Recorte espacial al AOI de las cuencas Nanay y Napo
4. Reprojeccion a EPSG:32718

#### Fase 2: Procesamiento y Clasificacion

**A. Deteccion de Bancos de Arena:**
- NDWI = (Green - NIR) / (Green + NIR)
- NDVI = (NIR - Red) / (NIR + Red)
- MNDWI = (Green - SWIR1) / (Green + SWIR1)
- Umbralizacion multiple: MNDWI [0.0-0.35], NDVI < 0.15, B4 [0.08-0.35], B11 < 0.12

**B. Deteccion de Mineria Aurifera:**
- Piscinas de decantacion: MNDWI 0.15-0.45, NIR < 0.10
- Zonas dragadas: NDVI < 0.12, SWIR1 > 0.08, ratio B5/B4 0.85-1.40
- Agua turbia: MNDWI 0-0.25, Red > 0.10
- Validacion con alertas GEOBOSQUES

**C. Analisis Multitemporal:**
- Rasters de cambio con 4 clases: perdida, ganancia, estable, sin presencia
- Metricas: area total, tasa de cambio, migracion de canales

#### Fase 3: Analisis Espacial y Estadistico
- Buffer analysis: zonas de influencia (500m, 1km, 2km)
- Overlay con comunidades nativas, ANP y titulos habilitantes
- Tablas de contingencia y correlacion espacial
""")

with tab3:
    st.markdown("""
### 3.5. Implementacion en Google Earth Engine

Toda la suite de procesamiento se implemento en 9 scripts modulares en GEE:

| Script | Nombre | Entrada | Salida |
|--------|--------|---------|--------|
| 00 | subir_shapes.py | SHP de ArcGIS Pro | Assets GEE: aoi_nanay, aoi_napo, cuencas_ana |
| 01 | delimitar_aoi.js | Assets aoi_nanay, aoi_napo | AOI unificado |
| 02 | descargar_sentinel2.js | AOI + coleccion S2 | Mosaicos Sentinel-2 (5 periodos) |
| 03 | indices_espectrales.js | Mosaicos S2 | NDVI, NDWI, MNDWI |
| 04 | deteccion_arena.js | Indices + S2 | Raster binario de bancos de arena |
| 05 | deteccion_mineria.js | Indices + S2 | Raster binario de mineria + vectores |
| 06 | analisis_multitemporal.js | Arena + Mineria 2019/2025 | Rasters de cambio |
| 07 | exportar_resultados.js | Todos los assets | GeoTIFF, SHP a Google Drive |
| 08 | estadisticas_dashboard.js | Todos los assets | 4 CSVs para dashboard |

### Flujo de ejecucion
1. Ejecutar 00_subir_shapes.py (local, una sola vez)
2. Ejecutar Scripts 01 al 08 en orden numerico en GEE Code Editor
3. Cada script encola tareas de exportacion en la pestana Tasks
4. Los resultados finales se descargan de Google Drive

Ver la pagina **Flujo de Trabajo** para el diagrama completo.
""")

st.divider()
st.caption("Grupo 03: Los Jaguares | Mapaton Regional 2026 - Fase Presencial Iquitos")
