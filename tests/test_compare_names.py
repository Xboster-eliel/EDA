import os
import pytest
from EDA.compare_names import (
    listar_svg,
    leer_shp_nombres,
    limpiar_nombre_svg,
    limpiar_nombre_shp,
    similitud,
    comparar,
)

def test_listar_svg(tmp_path):
    # Prepara carpeta con .svg y otros
    folder = tmp_path / "icons"
    folder.mkdir()
    for name in ["a.svg", "B.SVG", "c.txt", "d.svg"]:
        (folder / name).write_text("")
    result = listar_svg(str(folder))
    assert set(result) == {"a.svg", "B.SVG", "d.svg"}

def test_limpiar_nombre_svg():
    assert limpiar_nombre_svg("Ciclo_Anual_Abejorral.svg") == "Abejorral"
    assert limpiar_nombre_svg("mapa_xyz.svg") == "xyz"

def test_limpiar_nombre_shp():
    assert limpiar_nombre_shp("SAN MIGUEL [23050100]") == "SAN MIGUEL"
    assert limpiar_nombre_shp("Municipio") == "Municipio"

def test_similitud():
    assert similitud("hola", "hola") == 1.0
    assert 0.0 <= similitud("hola", "adiós") < 0.6

def test_comparar(monkeypatch):
    # Forzamos una lista fija de SVGs y nombres de shp
    monkeypatch.setattr("EDA.compare_names.listar_svg", lambda ruta, ext=".svg": ["A.svg", "B.svg"])
    monkeypatch.setattr("EDA.compare_names.leer_shp_nombres", lambda ruta, columna="NOMBRE": ["A", "C"])
    altos, medios = comparar("dummy_path", "dummy.shp", high=0.9, low=0.5)

    # ‘A’ vs ‘A’ debe ser alta coincidencia
    assert altos == [("a", "a", 1.0)]
    # ‘B’ vs ‘C’ debería aparecer en medios (ratio ~0.0x)
    assert all(low := 0.5 <= score < 0.9 for *_, score in medios)
