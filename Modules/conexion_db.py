"""
Módulo de conexión a SQL Server.
Intenta varios drivers ODBC y devuelve una conexión abierta o lanza
una excepción si ninguno funciona.
"""
from __future__ import annotations

import pyodbc

# Drivers más comunes en Windows
_DRIVERS = [
    "SQL Server Native Client 11.0",
    "SQL Server Native Client 10.0",
    "SQL Server",
]

# Ajusta aquí tu servidor y base de datos
_SERVER = "SQL01"
_DATABASE = "Gestion"


def obtener_conexion() -> pyodbc.Connection:
    """
    Devuelve una conexión a SQL Server usando autenticación integrada
    de Windows (Trusted_Connection=yes).
    """
    for driver in _DRIVERS:
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={_SERVER};"
            f"DATABASE={_DATABASE};"
            "Trusted_Connection=yes;"
        )
        try:
            return pyodbc.connect(conn_str, timeout=5)
        except pyodbc.Error:
            # Prueba con el siguiente driver
            continue

    raise ConnectionError(
        "❌ No se pudo establecer conexión con SQL Server. "
        "Verifica drivers instalados y credenciales."
    )
