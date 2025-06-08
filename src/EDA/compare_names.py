# compare_names.py
import os
from difflib import SequenceMatcher
from typing import List, Tuple, Set

# ---------- 1. Lectura de datos ---------- #
def listar_svg(ruta_carpeta: str, extension: str = ".svg") -> List[str]:
    """Devuelve la lista de archivos con la extensión dada dentro de la carpeta."""
    return [
        f for f in os.listdir(ruta_carpeta)
        if f.lower().endswith(extension.lower())
    ]

def leer_shp_nombres(
    ruta_shp: str,
    columna: str = "NOMBRE",
    lector_gpd=None
) -> List[str]:
    """
    Extrae la columna de nombres de un shapefile usando geopandas o un lector inyectado.
    """
    gpd = lector_gpd if lector_gpd else __import__("geopandas")
    gdf = gpd.read_file(ruta_shp)
    return gdf[columna].tolist()

# ---------- 2. Limpieza de nombres ---------- #
def limpiar_nombre_svg(nombre_archivo: str) -> str:
    base = os.path.splitext(nombre_archivo)[0]
    return base.split("_")[-1].strip()  # parte tras el último guión bajo

def limpiar_nombre_shp(nombre: str) -> str:
    return nombre.split(" [")[0].strip()  # elimina código entre corchetes

# ---------- 3. Comparación ---------- #
def similitud(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def comparar(
    carpeta_svg: str,
    ruta_shp: str,
    high: float = 0.85,
    low: float = 0.60,
) -> Tuple[List[Tuple[str, str, float]], List[Tuple[str, str, float]]]:
    """Core: compara nombres del folder vs. shapefile y los clasifica."""
    svg_raw  = listar_svg(carpeta_svg)
    shp_raw  = leer_shp_nombres(ruta_shp)

    svg = {limpiar_nombre_svg(n).lower()  for n in svg_raw}
    shp = {limpiar_nombre_shp(n).lower() for n in shp_raw}

    altos, medios = [], []
    for s in svg:
        for h in shp:
            r = similitud(s, h)
            if r >= high:
                altos.append((s, h, round(r, 3)))
            elif low <= r < high:
                medios.append((s, h, round(r, 3)))
    return altos, medios
