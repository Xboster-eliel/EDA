# compare_names.py  (versión documentada)
from __future__ import annotations
import os
from difflib import SequenceMatcher
from typing import List, Tuple, Set
import geopandas as gpd

def listar_svg(ruta_carpeta: str, extension: str = ".svg") -> List[str]:
    """
    Lista archivos con una extensión específica.

    Args:
        ruta_carpeta: Carpeta donde buscar.
        extension: Extensión a filtrar ('.svg', '.png', etc.).

    Returns:
        Lista de nombres de archivo que cumplen el filtro.

    Example:
        >>> listar_svg("/data/icons")
        ['Ciclo_Anual_Abejorral.svg', 'Ciclo_Anual_Rionegro.svg']
    """
    return [
        f for f in os.listdir(ruta_carpeta)
        if f.lower().endswith(extension.lower())
    ]

def leer_shp_nombres(
    ruta_shp: str,
    columna: str = "NOMBRE",
) -> List[str]:
    """
    Extrae una columna de texto de un shapefile.

    Args:
        ruta_shp: Ruta al .shp (o geopackage).
        columna: Campo a extraer con los nombres.

    Returns:
        Lista con los valores de la columna indicada.

    Example:
        >>> leer_shp_nombres("cuencas.shp", "NOMBRE")[:3]
        ['MAGDALENA', 'ATRATO', 'CAUCA']
    """
    gdf = gpd.read_file(ruta_shp)
    return gdf[columna].astype(str).tolist()

def limpiar_nombre_svg(nombre_archivo: str) -> str:
    """
    Limpia el nombre de un archivo SVG.

    Regla: toma la parte posterior al último '_' y elimina la extensión.

    Example:
        >>> limpiar_nombre_svg("Ciclo_Anual_Abejorral.svg")
        'Abejorral'
    """
    base = os.path.splitext(nombre_archivo)[0]
    return base.split("_")[-1].strip()

def limpiar_nombre_shp(nombre: str) -> str:
    """
    Limpia el campo 'NOMBRE' de un shapefile, quitando códigos en corchetes.

    Example:
        >>> limpiar_nombre_shp("SAN MIGUEL [23050100]")
        'SAN MIGUEL'
    """
    return nombre.split(" [")[0].strip()

def similitud(a: str, b: str) -> float:
    """
    Calcula la similitud de dos cadenas usando *SequenceMatcher*.

    Returns:
        Valor entre 0 y 1. 1 == idéntico.
    """
    return SequenceMatcher(None, a, b).ratio()

def comparar(
    carpeta_svg: str,
    ruta_shp: str,
    high: float = 0.85,
    low: float = 0.60,
) -> Tuple[List[Tuple[str, str, float]], List[Tuple[str, str, float]]]:
    """
    Compara los nombres de archivos `.svg` con los del shapefile y los clasifica.

    Args:
        carpeta_svg: Carpeta que contiene los archivos `.svg`.
        ruta_shp: Ruta al shapefile para comparar.
        high: Umbral de “alta coincidencia”.
        low : Umbral mínimo para reportar “alguna coincidencia”.

    Returns:
        Tuple:
            - high_coincidence: lista de tuplas (svg, shp, ratio) con `ratio >= high`
            - some_coincidence: lista con `low <= ratio < high`

    Example (uso rápido):
        >>> altos, medios = comparar("./svgs", "cuencas.shp")
        >>> len(altos), len(medios)
        (12, 7)
    """
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
