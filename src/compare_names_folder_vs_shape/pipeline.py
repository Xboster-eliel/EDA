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
    low_thresh: float = 0.60,
    verbose: bool = True
) -> tuple[set[str], set[str]]:
    """
    Orquesta todo el flujo y, si verbose=True, imprime el detalle.

    Args:
        svg_dirs: Lista de rutas de carpetas con .svg.
        shapefile_path: Ruta al .shp.
        gdf_col: Nombre de la columna del GeoDataFrame a limpiar.
        mount_drive: Si True, monta Google Drive.
        mount_point: Punto de montaje.
        high_thresh: Umbral para 'high_coincidence'.
        low_thresh: Umbral mínimo para 'some_coincidence'.
        verbose: Si True, imprime las secciones y bullets.
    Returns:
        high_set, some_set
    """
    # 1. Montar Drive
    if mount_drive:
        drive.mount(mount_point, force_remount=True)

    # 2. Leer y limpiar nombres SVG
    all_svgs = []
    for d in svg_dirs:
        all_svgs += leer_nombres_archivos_svg(d)
    unique_svgs = set(all_svgs)
    nombres_svg = {
        limpiar_nombre_estacion(os.path.splitext(f)[0]).lower()
        for f in unique_svgs
    }

    # 3. Cargar y limpiar shapefile
    gdf = gpd.read_file(shapefile_path)
    nombres_gdf = {
        limpiar_nombre_gdf(val).lower()
        for val in gdf[gdf_col]
    }

    # 4. Comparación detallada
    high_coincidence = []
    some_coincidence = []
    for svg in nombres_svg:
        for gdf_name in nombres_gdf:
            r = similitud(svg, gdf_name)
            if r >= high_thresh:
                high_coincidence.append((svg, gdf_name, round(r, 3)))
            elif r >= low_thresh:
                some_coincidence.append((svg, gdf_name, round(r, 3)))

    # 5. Conjuntos finales
    high_set = {a for a, b, _ in high_coincidence}
    some_set = {a for a, b, _ in some_coincidence}

    # 6. Impresión del informe (igual que antes)
    if verbose:
        print("=== HIGH COINCIDENCE (ratio ≥ {:.2f}) ===".format(high_thresh))
        for a, b, r in high_coincidence:
            print(f"  • '{a}'  ⟷  '{b}'  =>  {r}")
        print("\n=== SOME COINCIDENCE ({:.2f} ≤ ratio < {:.2f}) ===".format(low_thresh, high_thresh))
        for a, b, r in some_coincidence:
            print(f"  • '{a}'  ⟷  '{b}'  =>  {r}")
        print("\n***NOMBRES EN LA CARPETA ||||||||||||| NOMBRES DEL SHAPE CARGADO***")
        print("Nombres en high_coincidence_set:", high_set)
        print("Nombres en some_coincidence_set:", some_set)

    return high_set, some_set
