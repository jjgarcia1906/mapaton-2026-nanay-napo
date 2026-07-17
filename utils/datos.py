"""
Carga de Datos — Dashboard Mapatón 2026
Lee los CSVs exportados desde Google Earth Engine (Script 08).
"""

import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def cargar_datos():
    """Carga todos los CSVs y retorna un diccionario de DataFrames."""
    dfs = {}

    archivos = {
        "bancos": "Estadisticas_BancosArena.csv",
        "mineria": "Estadisticas_Mineria.csv",
        "serie": "Serie_Temporal.csv",
        "correlacion": "Correlacion_Proximidad.csv",
    }

    for clave, archivo in archivos.items():
        ruta = os.path.join(DATA_DIR, archivo)
        if os.path.isfile(ruta):
            dfs[clave] = pd.read_csv(ruta)
        else:
            dfs[clave] = _generar_datos_dummy(clave)

    return dfs


def filtrar_datos(df, ano=None, cuenca=None):
    """Filtra DataFrame por año y/o cuenca."""
    resultado = df.copy()
    if ano is not None and "ano" in resultado.columns:
        resultado = resultado[resultado["ano"] == int(ano)]
    if cuenca and cuenca != "Todas" and "cuenca" in resultado.columns:
        resultado = resultado[resultado["cuenca"].str.upper() == cuenca.upper()]
    return resultado


def _generar_datos_dummy(clave):
    """Genera datos de ejemplo mientras no lleguen los CSVs reales de GEE."""
    import numpy as np

    anos = [2019, 2021, 2023, 2024, 2025]
    cuencas = ["Nanay", "Napo"]

    if clave == "bancos":
        rows = []
        for a in anos:
            for c in cuencas:
                rows.append({"ano": a, "cuenca": c, "area_ha": np.random.uniform(400, 900)})
            rows.append({"ano": a, "cuenca": "TOTAL", "area_ha": np.random.uniform(900, 1700)})
        return pd.DataFrame(rows)

    elif clave == "mineria":
        rows = []
        for a in anos:
            for c in cuencas:
                rows.append({"ano": a, "cuenca": c, "area_ha": np.random.uniform(10, 150)})
            rows.append({"ano": a, "cuenca": "TOTAL", "area_ha": np.random.uniform(30, 250)})
        return pd.DataFrame(rows)

    elif clave == "serie":
        rows = []
        for a in anos:
            rows.append({
                "ano": a,
                "arena_ha": np.random.uniform(900, 1700),
                "mineria_ha": np.random.uniform(30, 250),
            })
        return pd.DataFrame(rows)

    elif clave == "correlacion":
        return pd.DataFrame({
            "buffer_m": [500, 1000, 2000, 5000],
            "arena_perdida_ha": [45, 120, 230, 380],
        })

    return pd.DataFrame()
