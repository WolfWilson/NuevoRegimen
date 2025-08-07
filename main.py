#!/usr/bin/env python
# coding: utf-8
"""
Gestor de Régimen – PyQt5
"""

import os
import sys
import pyodbc
from typing import Dict

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from PyQt5.QtGui import QIcon

from Modules.style import RoundedWindow
from Modules.resources import ICON_PATH
from Modules.conexion_db import obtener_conexion

# ────────────────────────────────────────────────────────────────
# Mapeo id  →  nombre del régimen
REGIMENES: Dict[int, str] = {1: "Docentes", 2: "Régimen Común", 3: "Régimen Policial"}
# ────────────────────────────────────────────────────────────────


class MainWindow(RoundedWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Gestión de Régimen")
        self.setGeometry(100, 100, 400, 320)

        # Ícono de la ventana
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        else:
            print(f"⚠️  Ícono no encontrado: {ICON_PATH}")

        # ───── Layout principal ─────
        layout = QVBoxLayout(self)

        # Entrada de CUIL
        layout.addWidget(QLabel("Ingrese CUIL:"))
        self.cuil_input = QLineEdit()
        self.cuil_input.setPlaceholderText("CUIL (11 dígitos)")
        layout.addWidget(self.cuil_input)

        # Botón Buscar
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_persona)
        layout.addWidget(btn_buscar)

        # Etiquetas de resultado
        self.label_nombre = QLabel("Nombre:")
        self.label_fec_nac = QLabel("Fecha de Nacimiento:")
        self.label_regimen_actual = QLabel("Régimen Actual:")
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.label_fec_nac)
        layout.addWidget(self.label_regimen_actual)

        # Selector de régimen
        layout.addWidget(QLabel("Seleccione Nuevo Régimen:"))
        self.regimen_combo = QComboBox()
        for id_, nombre in REGIMENES.items():
            self.regimen_combo.addItem(nombre, id_)
        layout.addWidget(self.regimen_combo)

        # Botón Guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_regimen)
        layout.addWidget(btn_guardar)

    # ═════════ UTILIDADES ═════════
    def mostrar_mensaje(
        self,
        titulo: str,
        mensaje: str,
        icon: QMessageBox.Icon = QMessageBox.Information,
    ) -> None:
        QMessageBox(icon, titulo, mensaje, parent=self).exec()

    def _cuil_valido(self, cuil: str) -> bool:
        return cuil.isdigit() and len(cuil) == 11

    # ═════════ CONSULTAS ═════════
    def buscar_persona(self) -> None:
        """Consulta datos personales y régimen actual por CUIL."""
        cuil = self.cuil_input.text().strip()

        if not self._cuil_valido(cuil):
            self.mostrar_mensaje(
                "Error", "El CUIL debe tener exactamente 11 dígitos numéricos.", QMessageBox.Warning
            )
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # Datos personales
            cursor.execute("EXEC Gestion.dbo.Anto_ObtenerPersonaPorCUIL @CUIL = ?", cuil)
            persona = cursor.fetchone()
            if persona:
                nombre = persona.Apeynom
                fecha_nac = (
                    persona.Fec_nac.strftime("%d/%m/%Y") if persona.Fec_nac else "No disponible"
                )
                self.label_nombre.setText(f"Nombre: {nombre}")
                self.label_fec_nac.setText(f"Fecha de Nacimiento: {fecha_nac}")
            else:
                self.label_nombre.setText("Nombre: No encontrado")
                self.label_fec_nac.setText("Fecha de Nacimiento: No encontrado")

            # Régimen actual
            cursor.execute("EXEC Gestion.dbo.anto_regimenactual @CUIL = ?", cuil)
            reg = cursor.fetchone()
            if reg:
                reg_id = int(reg.REGIMEN)
                reg_nombre = REGIMENES.get(reg_id, "Desconocido")
                self.label_regimen_actual.setText(f"Régimen Actual: {reg_id} – {reg_nombre}")
            else:
                self.label_regimen_actual.setText("Régimen Actual: No encontrado")

        except pyodbc.Error as e:
            print("Error al ejecutar la consulta:", e)
            self.mostrar_mensaje("Error", "No se pudo obtener los datos.", QMessageBox.Critical)
        finally:
            conn.close()

    # ═════════ ACTUALIZAR ═════════
    def guardar_regimen(self) -> None:
        """Actualiza el régimen y refresca la vista."""
        cuil = self.cuil_input.text().strip()
        nuevo_regimen = int(self.regimen_combo.currentData())

        if not self._cuil_valido(cuil):
            self.mostrar_mensaje(
                "Error", "El CUIL debe tener exactamente 11 dígitos numéricos.", QMessageBox.Warning
            )
            return

        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute(
                "EXEC Gestion.dbo.Anto_CambiarRegimen @CUIL = ?, @NuevoRegimen = ?", cuil, nuevo_regimen
            )
            conn.commit()

            self.mostrar_mensaje("Éxito", "Régimen actualizado correctamente.")

            # 🔄  Refrescar datos en pantalla
            self.buscar_persona()

        except pyodbc.Error as e:
            print("Error al ejecutar el procedimiento almacenado:", e)
            self.mostrar_mensaje("Error", "No se pudo actualizar el régimen.", QMessageBox.Critical)
        finally:
            conn.close()


# ═════════ MAIN ═════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
