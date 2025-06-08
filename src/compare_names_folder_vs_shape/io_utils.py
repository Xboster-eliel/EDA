# my_lib/io_utils.py

import os
import geopandas as gpd
import difflib

def leer_nombres_archivos_svg(ruta_carpeta):
    """
    Lee los nombres de los archivos .svg en una carpeta y los devuelve como una lista.
    Args:
        ruta_carpeta: La ruta de la carpeta a escanear.
    Returns:
        Una lista de nombres de archivos .svg en la carpeta especificada.
    """
    nombres = []
    for f in os.listdir(ruta_carpeta):
        if f.endswith('.svg'):
            nombres.append(f)
    return nombres

def limpiar_nombre_estacion(nombre_sin_ext):
    """
    De "Ciclo_Anual_Abejorral (2)" → "Abejorral (2)"
    """
    idx = nombre_sin_ext.rfind("_")
    return nombre_sin_ext[idx+1:].strip() if idx != -1 else nombre_sin_ext.strip()

def limpiar_nombre_gdf(nombre_con_codigo):
    """
    De "SAN MIGUEL [23050100]" → "SAN MIGUEL"
    """
    return nombre_con_codigo.split(' [')[0].strip() if '[' in nombre_con_codigo else nombre_con_codigo.strip()

def similitud(a: str, b: str) -> float:
    """
    Ratio de similitud entre dos cadenas (0.0–1.0).
    """
    return difflib.SequenceMatcher(None, a, b).ratio()
