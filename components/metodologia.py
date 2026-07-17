"""
Componente de Metodologia - Dashboard Mapaton 2026
Explica como se hizo el analisis para cualquier persona.
"""
import streamlit as st

def renderizar_metodologia():
    st.header("Metodologia del Estudio")

    tab1, tab2, tab3, tab4 = st.tabs(["Datos", "Metodo", "Indicadores", "Herramientas"])

    with tab1:
        st.subheader("Insumos Utilizados")
        st.markdown("""
| Insumo | Fuente | Caracteristica |
|--------|-------|----------------|
| Imagenes Sentinel-2 | ESA (Agencia Espacial Europea) | 10 m de resolucion, 8 bandas espectrales. Periodos de vaciante (agos-nov) 2019-2025. |
| Red hidrografica | GORE Loreto - Datos Fundamentales | Rios principales, cuencas del Nanay y Napo |
""")

        st.info("Por que solo epoca de vaciante? De agosto a noviembre el nivel del rio baja y los bancos de arena quedan expuestos, lo que permite verlos desde el satelite. En creciente estan bajo el agua.")

    with tab2:
        st.subheader("Metodo de Analisis")
        st.markdown("""
### Flujo de procesamiento

1. Descarga de imagenes: Google Earth Engine filtra ~146 escenas Sentinel-2 por año, seleccionando solo aquellas con menos del 20% de nubes sobre las cuencas Nanay y Napo.

2. Enmascaramiento de nubes: Mediante la banda QA60 de Sentinel-2 se eliminan pixel por pixel las nubes y sombras restantes, generando un mosaico limpio por año (mediana de todas las escenas).

3. Calculo de indices espectrales:
   - NDVI (vegetacion): diferencia entre infrarrojo cercano y rojo
   - NDWI (agua): diferencia entre verde e infrarrojo cercano
   - MNDWI (sedimentos): diferencia entre verde e infrarrojo medio

4. Clasificacion de arena: Cada pixel debe cumplir 4 condiciones simultaneas:
   - MNDWI entre 0.0 y 0.35 (arena humeda, no agua profunda)
   - NDVI menor a 0.15 (sin vegetacion)
   - Banda roja entre 0.08 y 0.35 (superficie clara)
   - SWIR menor a 0.12 (arena limpia, no suelo oscuro)

5. Deteccion de mineria: Se buscan 3 tipos de evidencia:
   - Piscinas de decantacion (agua turbia en formas geometricas)
   - Zonas dragadas (suelo expuesto sin vegetacion)
   - Agua con sedimentos en suspension (canales de lavado)

### Como sabemos que es mineria y no arena natural?

Usamos firmas espectrales: cada material refleja la luz de forma distinta segun su composicion. Un pixel de arena blanca y un pixel de piscina minera se ven similares al ojo humano, pero el satelite Sentinel-2 capta 8 bandas del espectro electromagnetico, incluyendo infrarrojo que nosotros no vemos.

| Banda espectral | Arena de playa | Piscina minera | Por que? |
|-----------------|:---:|:---:|-----------|
| Rojo (B4) | Medio-Alto | Medio | La arena refleja mas luz visible |
| NIR (B8) | Bajo | Muy bajo | El agua absorbe todo el infrarrojo |
| SWIR (B11) | Muy bajo | Medio | La arena limpia no tiene minerales que reflejen SWIR |
| MNDWI | 0.0-0.35 | 0.15-0.45 | La piscina tiene agua mas profunda que la arena humeda |

La clave esta en el SWIR (B11): la arena de rio es cuarzo casi puro que absorbe el infrarrojo medio, mientras que el suelo removido por mineria expone arcillas y oxidos de hierro que SI reflejan en SWIR. Esa diferencia de apenas 0.04 en reflectancia es lo que permite separar playa natural de zona minera.

6. Analisis de cambio: Comparacion directa de los mapas de 2019 vs 2025 para cuantificar perdida, ganancia y persistencia de arena y mineria.
""")

    with tab3:
        st.subheader("Indicadores Clave")
        st.markdown("""
| Indicador | Que mide | Como se lee |
|-----------|----------|-------------|
| Bancos de Arena (ha) | Superficie de playas detectadas | Mas hectareas = mayor exposicion de arena en vaciante |
| Mineria Detectada (ha) | Area con evidencia de mineria aurifera | Mas hectareas = mayor actividad minera |
| Mineria vs Arena (%) | Proporcion entre mineria y playas | >10% indica presion alta sobre el ecosistema |
| Evolucion Temporal | Cambio de ambos indicadores en 6 años | Tendencia creciente = expansion del fenomeno |
| Correlacion Proximidad | Arena perdida cerca de zonas mineras | Mide la relacion espacial mineria-degradacion |
""")

    with tab4:
        st.subheader("Herramientas y Plataformas")
        st.markdown("""
| Herramienta | Uso |
|-------------|-----|
| Google Earth Engine | Procesamiento de imagenes satelitales en la nube (9 scripts JavaScript) |
| ArcGIS Pro | Cartografia, mosaicos y analisis espacial complementario |
| Streamlit + Folium + Plotly | Dashboard interactivo web |
| Python (rasterio, pandas, numpy) | Procesamiento local y generacion de estadisticas |
""")

        st.success("Reproducibilidad: Todos los scripts de GEE, codigos Python y datos estan documentados y disponibles en el repositorio del proyecto. El analisis puede repetirse para cualquier otro periodo o cuenca de la Amazonia peruana.")
