#!/usr/bin/env python
# coding: utf-8
"""
Gestor de Régimen – PyQt5
"""

import os
import sys
import pyodbc
from typing import Dict, Optional

from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
    QDesktopWidget,
)
from PyQt5.QtGui import QIcon

from Modules.style import RoundedWindow
from Modules.resources import ICON_PATH
from Modules.conexion_db import obtener_conexion

# ────────────────────────────────────────────────────────────────
REGIMENES: Dict[int, str] = {1: "Docentes", 2: "Régimen Común", 3: "Régimen Policial"}
# ────────────────────────────────────────────────────────────────


class MainWindow(RoundedWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Gestión de Régimen")
        self.setFixedSize(340, 380)

        # Ícono
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

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

        # Etiquetas (fucsia) + valores (blanco)
        self.nom_tag = QLabel("Nombre:");              self.nom_tag.setObjectName("etiqueta")
        self.nom_val = QLabel("")
        self.fn_tag  = QLabel("Fecha de Nacimiento:"); self.fn_tag.setObjectName("etiqueta")
        self.fn_val  = QLabel("")
        self.reg_tag = QLabel("Régimen Actual:");      self.reg_tag.setObjectName("etiqueta")
        self.reg_val = QLabel("")

        for w in (
            self.nom_tag, self.nom_val,
            self.fn_tag, self.fn_val,
            self.reg_tag, self.reg_val,
        ):
            layout.addWidget(w)

        # Selector de régimen
        layout.addWidget(QLabel("Seleccione Nuevo Régimen:"))
        self.regimen_combo = QComboBox()
        for reg_id, nombre in REGIMENES.items():
            self.regimen_combo.addItem(nombre, reg_id)
        layout.addWidget(self.regimen_combo)

        # Botón Guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_regimen)
        layout.addWidget(btn_guardar)

    # ───────── Utilidades ─────────
    @staticmethod
    def _cuil_valido(cuil: str) -> bool:
        return cuil.isdigit() and len(cuil) == 11

    def mostrar_mensaje(
        self,
        titulo: str,
        mensaje: str,
        icon: QMessageBox.Icon = QMessageBox.Information,
    ) -> None:
        QMessageBox(icon, titulo, mensaje, parent=self).exec()

    # ───────── Consultas ─────────
    def buscar_persona(self) -> None:
        cuil = self.cuil_input.text().strip()
        if not self._cuil_valido(cuil):
            self.mostrar_mensaje("Error", "El CUIL debe tener 11 dígitos numéricos.", QMessageBox.Warning)
            return

        conn: Optional[pyodbc.Connection] = None
        try:
            conn = obtener_conexion()
            cur = conn.cursor()

            # Datos personales (DB cambiada a Aportes)
            cur.execute("EXEC Aportes.dbo.Anto_ObtenerPersonaPorCUIL @CUIL = ?", cuil)
            p = cur.fetchone()
            if p:
                # p.Fec_nac podría ser None o datetime/date
                fec_txt = "No disponible"
                try:
                    if getattr(p, "Fec_nac", None):
                        fec_txt = p.Fec_nac.strftime("%d/%m/%Y")
                except Exception:
                    # Si viene como string o formato raro
                    fec_txt = str(p.Fec_nac)
                self.nom_val.setText(getattr(p, "Apeynom", ""))
                self.fn_val.setText(fec_txt)
            else:
                self.nom_val.setText("No encontrado")
                self.fn_val.setText("No disponible")

            # Régimen actual (DB cambiada a Aportes)
            cur.execute("EXEC Aportes.dbo.anto_regimenactual @CUIL = ?", cuil)
            r = cur.fetchone()
            if r and getattr(r, "REGIMEN", None) is not None:
                reg_id = int(r.REGIMEN)
                self.reg_val.setText(f"{reg_id} – {REGIMENES.get(reg_id, 'Desconocido')}")
            else:
                self.reg_val.setText("No encontrado")

        except pyodbc.Error as e:
            print("Error SQL:", e)
            self.mostrar_mensaje("Error", "No se pudo obtener los datos.", QMessageBox.Critical)
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    # ───────── Actualizar ─────────
    def guardar_regimen(self) -> None:
        cuil = self.cuil_input.text().strip()
        nuevo_regimen = int(self.regimen_combo.currentData())

        if not self._cuil_valido(cuil):
            self.mostrar_mensaje("Error", "El CUIL debe tener 11 dígitos numéricos.", QMessageBox.Warning)
            return

        conn: Optional[pyodbc.Connection] = None
        try:
            conn = obtener_conexion()
            cur = conn.cursor()
            # Cambio a Aportes
            cur.execute(
                "EXEC Aportes.dbo.Anto_CambiarRegimen @CUIL = ?, @NuevoRegimen = ?",
                cuil, nuevo_regimen
            )
            conn.commit()
            self.mostrar_mensaje("Éxito", "Régimen actualizado correctamente.")
            self.buscar_persona()

        except pyodbc.Error as e:
            print("Error SQL:", e)
            self.mostrar_mensaje("Error", "No se pudo actualizar el régimen.", QMessageBox.Critical)
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass


def center_on_screen(window) -> None:
    """Centra la ventana en la pantalla principal."""
    screen = QDesktopWidget().screenGeometry()
    size = window.geometry()
    x = (screen.width() - size.width()) // 2
    y = (screen.height() - size.height()) // 2
    window.move(x, y)


# ───────── Main ─────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    center_on_screen(win)  # ← Centrar antes de mostrar
    win.show()
    # PyQt5 usa exec_()
    sys.exit(app.exec_())
