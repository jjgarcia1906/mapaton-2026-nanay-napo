"""
Pagina: Solucion - Dashboard Mapaton 2026
"""
import streamlit as st

st.set_page_config(page_title="Solucion | Mapaton 2026", page_icon="💡", layout="wide")

st.title("4. Solucion")

tab1, tab2, tab3, tab4 = st.tabs(["Aplicaciones", "Dashboard", "Indicadores", "Base de Datos"])

with tab1:
    st.markdown("""
### 4.1. Aplicaciones

Cinco lineas de aplicacion orientadas a resolver problemas reales del territorio amazonico:

#### 4.1.1. Sistema de Alerta Temprana para Fiscalizacion Ambiental
Los rasters de deteccion de mineria generados anualmente constituyen la base para un sistema de alerta temprana que notifique a las autoridades competentes sobre la aparicion de nuevos focos de mineria ilegal.

- Deteccion automatizada de nuevos poligonos de mineria por comparacion interanual
- Reportes geoespaciales con coordenadas, area afectada y fecha estimada
- Notificacion por correo electronico o integracion via API con sistemas institucionales

#### 4.1.2. Plataforma de Visualizacion Publica y Denuncia Ciudadana
El dashboard interactivo permite que comunidades nativas, periodistas y ciudadania accedan a informacion verificable sobre el estado de los rios.

- Capa de comunidades nativas con indicador de proximidad a zonas mineras
- Descarga de reportes en PDF con mapas y estadisticas
- Modo de visualizacion simplificado para usuarios sin formacion tecnica

#### 4.1.3. Aplicacion Movil de Monitoreo Participativo
Los datos pueden alimentar una aplicacion movil que permita a comuneros registrar observaciones en campo y contrastarlas con detecciones satelitales.

#### 4.1.4. Integracion con Geoportales Institucionales
Los productos cartograficos estan disenados para integrarse en geoportales como GEOBOSQUES, SIAR Loreto e IDEP.

#### 4.1.5. Aplicacion en Educacion Ambiental y Comunicacion
Material de alto impacto para campanas de educacion ambiental: Story Maps, infografias, timelapses.
""")

with tab2:
    st.markdown("""
### 4.2. Dashboard Interactivo

#### Tecnologia y Arquitectura

| Componente | Tecnologia | Rol |
|------------|-----------|-----|
| Frontend | Streamlit (Python) | Interfaz web interactiva |
| Mapas | Folium + Leafmap | Mapas con capas togglables |
| Graficos | Plotly | Graficos de linea, barras, dispersion |
| Datos | CSV + GeoJSON | Datos tabulares y geoespaciales |
| Despliegue | Streamlit Cloud | Hosting gratuito, URL publica |

#### Funcionalidades
- Filtrado dinamico: mapa, graficos y estadisticas se actualizan al cambiar año o cuenca
- Consulta espacial: clic en cualquier punto del mapa muestra informacion detallada
- Comparacion lado a lado: modo split view para visualizar dos años simultaneamente
- Exportacion: descarga de tablas en CSV y mapas en PNG
""")

with tab3:
    st.markdown("""
### 4.3. Indicadores

#### Indicadores de Estado (bancos de arena)

| Codigo | Indicador | Unidad | Fuente |
|--------|-----------|--------|--------|
| I-01 | Area total de bancos de arena por cuenca | ha | Sentinel-2 + GEE |
| I-02 | Indice de fragmentacion de playas | poligonos/ha | Sentinel-2 + GEE |
| I-03 | Ancho promedio de bancos de arena | m | Sentinel-2 + GEE |

#### Indicadores de Presion (mineria)

| Codigo | Indicador | Unidad | Fuente |
|--------|-----------|--------|--------|
| I-04 | Area total de mineria detectada por cuenca | ha | Sentinel-2 + GEE |
| I-05 | Densidad de campamentos mineros | campamentos/km | Sentinel-2 + GEE |
| I-06 | Proximidad a comunidades nativas | km | GEE + GOREL |

#### Indicadores de Impacto (cambio)

| Codigo | Indicador | Unidad | Fuente |
|--------|-----------|--------|--------|
| I-07 | Tasa de perdida neta de bancos de arena | % | GEE Script 06 |
| I-08 | Correlacion mineria-perdida de arena | % | GEE Script 06 |
| I-09 | Superficie de ANP afectada por mineria | ha | GEE + SERNANP |
""")

with tab4:
    st.markdown("""
### 4.4. Base de Datos Geoespacial

Toda la informacion generada se consolida en una base de datos geoespacial estructurada, disenada para ser interoperable con ArcGIS Pro, QGIS y plataformas web.

#### Estructura

| Dataset | Tipo | Geometria | Periodicidad |
|---------|------|-----------|--------------|
| aoi_nanay_napo | Feature Class | Polygon | Estatico |
| bancos_arena_2019...2025 | Feature Class | Polygon | Anual (vaciante) |
| mineria_2019...2025 | Feature Class | Polygon | Anual (vaciante) |
| cambio_arena_2019_2025 | Raster | - | Multitemporal |
| cambio_mineria_2019_2025 | Raster | - | Multitemporal |
| comunidades_afectadas | Feature Class | Point | Actualizacion anual |
| indicadores_serie_temporal | Tabla | - | Anual |
| rgb_sentinel2_composites | Raster | - | Anual (mosaico vaciante) |

#### Metadatos
Cada dataset incluye metadatos normalizados segun el perfil ISO 19115 (LAMP), documentando titulo, fecha, escala, CRS, fuente, metodo y responsable tecnico.

#### Acceso
- Vectorial: Shapefile (.shp) y GeoJSON
- Raster: GeoTIFF (Cloud Optimized - COG) con compresion LZW
- Tablas: CSV UTF-8
- Carpeta de descarga: Google Drive del proyecto
""")

st.divider()
st.caption("Grupo 03: Los Jaguares | Mapaton Regional 2026 - Fase Presencial Iquitos")
