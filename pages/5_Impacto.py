"""
Pagina: Impacto - Dashboard Mapaton 2026
"""
import streamlit as st

st.set_page_config(page_title="Impacto | Mapaton 2026", page_icon="🎯", layout="wide")

st.title("5. Impacto Esperado")

st.markdown("""
### 5.1. Usuarios Objetivo

| Usuario | Necesidad | Producto que recibe |
|---------|-----------|---------------------|
| Autoridades ambientales (MINAM, GOREL, ANA) | Evidencia geoespacial para fiscalizacion | Dashboard + Indicadores + Shapefiles |
| Fiscalias ambientales (FEMA) | Localizacion precisa de actividades ilegales | Shapefiles de mineria + mapas de cambio |
| Comunidades nativas y federaciones indigenas | Informacion sobre afectacion a sus territorios | Dashboard publico + Indicador I-06, I-09 |
| SERNANP y gestores de ANP | Monitoreo de presion minera en zonas de amortiguamiento | Indicador I-09 + raster intersectado |
| Academia e investigadores | Datos abiertos para estudios complementarios | Base de datos geoespacial + metadatos |
| Publico general y periodismo | Visualizacion comprensible del problema | Dashboard interactivo publico |

### 5.2. Resultados Esperados a Corto Plazo

- Mapas de distribucion de bancos de arena y mineria para 5 periodos (2019-2025)
- Dashboard interactivo funcional desplegado en la nube
- Base de datos geoespacial consolidada con metadatos, lista para integracion institucional

### 5.3. Sostenibilidad del Proyecto

La metodologia es replicable y escalable a otras cuencas de la Amazonia peruana (Ucayali, Madre de Dios, Maranon). El uso de datos abiertos (Sentinel-2 del programa Copernicus) y plataformas gratuitas (Google Earth Engine, Streamlit) garantiza que el monitoreo pueda continuar sin costos de licencias.

Los scripts de GEE desarrollados quedan documentados y disponibles para su reutilizacion por otros equipos tecnicos.
""")

st.divider()

st.title("6. Referencias")

refs = [
    "McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. International Journal of Remote Sensing, 17(7), 1425-1432.",
    "Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. NASA Special Publication, 351, 309.",
    "Xu, H. (2006). Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. International Journal of Remote Sensing, 27(14), 3025-3033.",
    "Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment, 202, 18-27.",
    "Asner, G. P., Llactayo, W., Tupayachi, R., & Luna, E. R. (2013). Elevated rates of gold mining in the Amazon revealed through high-resolution monitoring. PNAS, 110(46), 18454-18459.",
    "MINAM - GEOBOSQUES. (2024). Plataforma de monitoreo de cambios sobre la cobertura de los bosques. Peru.",
    "ESA - Copernicus. (2024). Sentinel-2 User Handbook. European Space Agency.",
    "ANA - Autoridad Nacional del Agua. (2023). Delimitacion de cuencas hidrograficas del Peru."
]
for i, ref in enumerate(refs, 1):
    st.markdown(f"{i}. {ref}")

st.divider()
st.caption("Grupo 03: Los Jaguares | Mapaton Regional 2026 - Fase Presencial Iquitos")
