# Modules/resources.py
from __future__ import annotations

import os
import sys


def _base_dir() -> str:
    """
    Devuelve la carpeta base donde buscar recursos.

    • En ejecución normal   → carpeta raíz del proyecto.
    • Con PyInstaller       → carpeta temporal _MEIPASS.
    """
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS  # type: ignore[attr-defined]
    # …/NuevoRegimen/Modules  →  …/NuevoRegimen
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def resource_path(*parts: str) -> str:
    """Forma una ruta absoluta compatible con PyInstaller."""
    return os.path.join(_base_dir(), *parts)


# 👉 Ruta al icono principal
ICON_PATH = resource_path("Source", "panda.png")

# 👉 Ruta a la hoja de estilos QSS
QSS_PATH = resource_path("UI", "style.qss")
