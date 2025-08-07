#Modules.py modulo de estilo principal

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox

class RoundedWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Window)  # type: ignore[attr-defined]
        self.setStyleSheet(STYLE)  # Aplica el estilo CSS
        self.dragging = False  # Para manejar el arrastre de la ventana
        self.offset = QPoint()  # Para guardar la posición inicial del mouse

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: # type: ignore[attr-defined]
            self.dragging = True
            self.offset = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()



STYLE = """
    QWidget {
        background: qlineargradient(
            x1: 0, y1: 0, 
            x2: 1, y2: 1,
            stop: 0 #434343, stop: 1 #434343
        );
        color: white;
        font-weight: normal;
    }

    QPushButton {
        background-color: #434343;
        color: white;
        border: 1px solid #DFFCFE;
        padding: 10px;
        border-radius: 8px;
        font-weight: normal;
        
    }

    QPushButton:hover {
        background-color: #C9A3BC;
        color: white;
        border: 1px solid #FFFFFF;
        
        
    }




    QPushButton:pressed {
        background-color: #E7DCE7;
    }

    QLabel {
        color: white;
        font-weight: normal;
    }

    QProgressBar {
        border: 2px solid #E7DCE7;
        border-radius: 5px;
        background: #E7DCE7;
        color: white;
        font-weight: normal;
    }

    QProgressBar::chunk {
        background-color: #E7DCE7;
        width: 20px;
    }
"""

# Función para mostrar una ventana emergente con el mensaje de completado
def show_completion_popup(parent, time_elapsed):
    msg = QMessageBox(parent)
    msg.setWindowTitle("Operación Completada")
    msg.setText(f"La copia ha finalizado en {time_elapsed:.2f} segundos.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.setIcon(QMessageBox.Icon.Information)

    # Aplicar estilo personalizado
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #1c1c1c;
            color: white;
            font-weight: normal;
        }
        QPushButton {
            background-color: #2d2d3c;
            color: white;
            border: 1px solid #3d3d5c;
            padding: 10px;
            border-radius: 5px;
            font-weight: normal;
        }
        QPushButton:hover {
            background-color: #3a3a50;
        }
        QPushButton:pressed {
            background-color: #1f1f2e;
        }
    """)

    msg.exec()


STYLE = """
    /* Estilo para el fondo de la ventana */
    QDialog, QWidget {
        background-color: #434343;
        border-radius: 15px; /* Bordes redondeados de la ventana */
        color: white;
        font-weight: normal;
    }

    /* Estilo para los botones */
    QPushButton {
        background-color: #434343;
        color: white;
        border: 1px solid #FFFFFF;
        padding: 10px;
        border-radius: 10px; /* Bordes redondeados para los botones */
        font-weight: normal;
        
    }

    QPushButton:hover {
        background-color: #C9A3BC;
        color: white;
        border: 1px solid #FFFFFF;
       
    }

    QPushButton:pressed {
        background-color: #E7DCE7;
    }

    QLabel {
        color: white;
        font-weight: normal;
    }

    QLineEdit, QComboBox {
        background-color: #1c1c1c;
        color: white;
        border: 1px solid #FFFFFF;
        padding: 5px;
        border-radius: 5px; /* Bordes redondeados en campos de entrada */
        font-weight: normal;
    }
    
    QDateEdit {
    background-color: #1c1c1c;
    color: white;
    border: 1px solid #DFFCFE; /* Borde claro */
    padding: 5px;
    border-radius: 5px; /* Bordes redondeados */
    font-weight: normal;
}

QDateEdit::drop-down {
    border: 5px; ; /* Sin borde en el icono desplegable */
}

QDateEdit::down-arrow {
    
    width: 12px;
    height: 12px;
}

QDateEdit::up-button, QDateEdit::down-button {
    width: 15px; /* tamaño de los botones arriba/abajo */
    border: 5px; /* sin borde en los botones de flecha */
}

    
    
"""
