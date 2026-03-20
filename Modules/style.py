# Modules/style.py – Carga el tema visual desde UI/style.qss

import os
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QDialog, QStyle, QStyleOption

from Modules.resources import QSS_PATH, ARROW_DOWN_PATH


def _cargar_qss() -> str:
    """Lee UI/style.qss y devuelve su contenido como string.
    Reemplaza el placeholder ARROW_DOWN_PATH con la ruta real del SVG."""
    if os.path.exists(QSS_PATH):
        with open(QSS_PATH, "r", encoding="utf-8") as f:
            qss = f.read()
        # Normalizar separadores para QSS (usa barras forward)
        arrow_path = ARROW_DOWN_PATH.replace("\\", "/")
        return qss.replace("__ARROW_DOWN_PATH__", arrow_path)
    return "QDialog, QWidget { background-color: #0d0f1a; color: #dde3f0; }"


# Capas del glow: (margen desde el borde, alpha 0-255)
# De afuera hacia adentro: difuso → sólido
_GLOW_LAYERS = [
    (3, 10),   # halo exterior, muy sutil
    (2, 30),   # capa media difusa
    (1, 70),   # capa interior semi-visible
    (0, 130),  # borde sólido principal
]
_GLOW_COLOR = QColor(0, 229, 255)   # cyan #00e5ff


class RoundedWindow(QDialog):
    """
    Ventana sin marco del sistema operativo con arrastre por clic y borde glow cyan.
    Carga el estilo desde UI/style.qss en cada instanciación.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)  # type: ignore[attr-defined]
        self.setStyleSheet(_cargar_qss())
        self.dragging = False
        self.offset = QPoint()

    def paintEvent(self, event) -> None:
        # 1. Dejar que QSS pinte el fondo (gradiente, etc.)
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)  # type: ignore[attr-defined]

        # 2. Dibujar las capas de glow sobre el fondo
        p.setRenderHint(QPainter.Antialiasing, False)  # type: ignore[attr-defined]
        p.setBrush(Qt.NoBrush)  # type: ignore[attr-defined]
        rect = self.rect()
        for margin, alpha in _GLOW_LAYERS:
            pen = QPen(QColor(_GLOW_COLOR.red(), _GLOW_COLOR.green(), _GLOW_COLOR.blue(), alpha))
            pen.setWidth(1)
            p.setPen(pen)
            p.drawRect(rect.adjusted(margin, margin, -margin - 1, -margin - 1))
        p.end()

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
