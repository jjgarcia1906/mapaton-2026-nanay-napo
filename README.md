# Dashboard Interactivo — Mapatón 2026

## Grupo 03: Los Jaguares
### Dinámica Fluvial y Minería Ilegal — Cuencas Nanay y Napo

---

## 🚀 Ejecución

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar dashboard
streamlit run app.py

# 3. Abrir en navegador
# http://localhost:8501
```

---

## 📁 Estructura del proyecto

```
dashboard/
├── app.py                  # Punto de entrada principal
├── requirements.txt        # Dependencias Python
├── .streamlit/
│   └── config.toml         # Tema y configuración
├── components/
│   ├── __init__.py
│   ├── filtros.py          # Selectores año/cuenca/capa
│   ├── mapa.py             # Mapa interactivo (Folium)
│   ├── graficos.py         # Gráficos temporales (Plotly)
│   └── estadisticas.py     # Tarjetas KPI
├── utils/
│   ├── __init__.py
│   └── datos.py            # Carga de CSVs (usa dummies si no hay datos reales)
├── data/
│   └── .gitkeep            # Acá se colocan los CSVs exportados de GEE
└── assets/
    └── (logos, imágenes)
```

---

## 📊 Datos necesarios

Colocar los siguientes archivos CSV en `data/`:

| Archivo | Origen | Descripción |
|---------|--------|-------------|
| `Estadisticas_BancosArena.csv` | GEE Script 08 | Área (ha) por año y cuenca |
| `Estadisticas_Mineria.csv` | GEE Script 08 | Área minera por año y cuenca |
| `Serie_Temporal.csv` | GEE Script 08 | Serie temporal consolidada |
| `Correlacion_Proximidad.csv` | GEE Script 08 | Correlación buffer-distancia |

**Si los CSVs no están disponibles**, el dashboard genera datos dummy automáticamente para pruebas.

---

## 🌐 Despliegue en la nube

### Opción 1: Streamlit Cloud (gratuito)
1. Subir el proyecto a GitHub
2. Conectar en https://streamlit.io/cloud
3. Desplegar con un clic

### Opción 2: Render.com (gratuito)
```bash
# requirements.txt debe incluir streamlit
# Comando de inicio: streamlit run app.py --server.port=$PORT
```
