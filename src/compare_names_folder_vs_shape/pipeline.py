# my_lib/pipeline.py

from google.colab import drive
import os
import geopandas as gpd

from .io_utils import (
    leer_nombres_archivos_svg,
    limpiar_nombre_estacion,
    limpiar_nombre_gdf,
    similitud
)

def run_comparison_pipeline(
    svg_dirs: list[str],
    shapefile_path: str,
    gdf_col: str,
    mount_drive: bool = True,
    mount_point: str = '/content/drive/',
    high_thresh: float = 0.85,
    low_thresh: float = 0.60
) -> tuple[set[str], set[str]]:
    """
    Orquesta todo el flujo de:
      1. Montar Drive (opcional).
      2. Leer y limpiar nombres SVG.
      3. Cargar y limpiar nombres del shapefile.
      4. Comparar similitud y devolver sets de coincidencias.

    Args:
        svg_dirs: Lista de rutas de carpetas con .svg.
        shapefile_path: Ruta al .shp.
        gdf_col: Nombre de la columna del GeoDataFrame a limpiar.
        mount_drive: Si True, monta Google Drive.
        mount_point: Punto de montaje.
        high_thresh: Umbral para 'high_coincidence'.
        low_thresh: Umbral mínimo para 'some_coincidence'.
    Returns:
        (high_set, some_set)
    """
    # 1. Montaje
    if mount_drive:
        drive.mount(mount_point, force_remount=True)

    # 2. SVGs
    all_svgs = []
    for d in svg_dirs:
        all_svgs += leer_nombres_archivos_svg(d)
    unique_svgs = set(all_svgs)

    nombres_svg = {
        limpiar_nombre_estacion(os.path.splitext(f)[0]).lower()
        for f in unique_svgs
    }

    # 3. Shapefile
    gdf = gpd.read_file(shapefile_path)
    nombres_gdf = {
        limpiar_nombre_gdf(val).lower()
        for val in gdf[gdf_col]
    }

    # 4. Comparación
    high, some = set(), set()
    for svg in nombres_svg:
        for gdf_name in nombres_gdf:
            r = similitud(svg, gdf_name)
            if r >= high_thresh:
                high.add(svg)
            elif r >= low_thresh:
                some.add(svg)

    return high, some
