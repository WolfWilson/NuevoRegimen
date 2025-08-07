# Modules/style.py – Estilo visual alternativo: elegante + profesionalidad

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog, QMessageBox


class RoundedWindow(QDialog):
    """
    Ventana con bordes redondeados y arrastre por clic.
    Aplica un estilo visual definido en STYLE.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(Qt.Window)  # type: ignore[attr-defined]
        self.setStyleSheet(STYLE)
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


def show_completion_popup(parent, time_elapsed: float) -> None:
    """
    Muestra un mensaje de confirmación estilizado.
    """
    msg = QMessageBox(parent)
    msg.setWindowTitle("Operación Completada")
    msg.setText(f"La operación finalizó en {time_elapsed:.2f} segundos.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStyleSheet(POPUP_STYLE)
    msg.exec()


# ──────────────────────────────────────────────────────────────────────
# 🎨 ESTILO PRINCIPAL – Elegancia Moderna
STYLE = """
QDialog, QWidget {
    background-color: #2b2d42;
    border-radius: 16px;
    color: #edf2f4;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}
QLabel#etiqueta {
    color: #ff1493;  /* Fucsia intenso */
    font-weight: bold;
}


QLabel {
    color: #edf2f4;
    font-weight: 500;
}

QPushButton {
    background-color: #8d99ae;
    color: #2b2d42;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: 600;  
}

QPushButton:hover {
    background-color: #a8b5cf;
}

QPushButton:pressed {
    background-color: #6c7a96;
}

QLineEdit, QComboBox {
    background-color: #1a1c2c;
    color: #edf2f4;
    border: 1px solid #8d99ae;
    padding: 6px;
    border-radius: 6px;
    font-weight: 500;
}

QDateEdit {
    background-color: #1a1c2c;
    color: #edf2f4;
    border: 1px solid #8d99ae;
    padding: 6px;
    border-radius: 6px;
}

QDateEdit::drop-down {
    border: none;
}

QDateEdit::down-arrow {
    width: 14px;
    height: 14px;
}

QDateEdit::up-button, QDateEdit::down-button {
    width: 14px;
    border: none;
}

QProgressBar {
    border: 1px solid #8d99ae;
    border-radius: 6px;
    background: #1a1c2c;
    color: #edf2f4;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #ef233c;
    width: 20px;
}
"""

# 💬 ESTILO PARA MENSAJES EMERGENTES
POPUP_STYLE = """
QMessageBox {
    background-color: #2b2d42;
    color: #edf2f4;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: normal;
}

QPushButton {
    background-color: #8d99ae;
    color: #2b2d42;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #a8b5cf;
}

QPushButton:pressed {
    background-color: #6c7a96;
}
"""
