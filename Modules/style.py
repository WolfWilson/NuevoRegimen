# Modules/style.py – Carga el tema visual desde UI/style.qss

import os
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog, QMessageBox

from Modules.resources import QSS_PATH


def _cargar_qss() -> str:
    """Lee UI/style.qss y devuelve su contenido como string."""
    if os.path.exists(QSS_PATH):
        with open(QSS_PATH, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback mínimo si el archivo no se encuentra
    return "QDialog, QWidget { background-color: #0d0f1a; color: #dde3f0; }"


class RoundedWindow(QDialog):
    """
    Ventana sin marco del sistema operativo con arrastre por clic.
    Carga el estilo desde UI/style.qss en cada instanciación.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # type: ignore[attr-defined]
        self.setStyleSheet(_cargar_qss())
        self.dragging = False
        self.offset = QPoint()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:  # type: ignore[attr-defined]
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if self.dragging:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self.dragging = False
        event.accept()
