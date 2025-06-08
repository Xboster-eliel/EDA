"""
API pública del paquete *compare_names_folder_vs_shape*.

Con una sola importación exponemos las piezas clave:

    >>> from compare_names_folder_vs_shape import run_comparison_pipeline
"""

from importlib.metadata import PackageNotFoundError, version

# Reexportamos la función de alto nivel
from .pipeline import run_comparison_pipeline

# Metadatos de versión PEP 566
try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    # Sucede en entornos sin instalar (editable mode, Colab, etc.)
    __version__ = "0.0.0"
__all__: list[str] = ["run_comparison_pipeline"]
