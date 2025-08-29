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
_DATABASE = "Aportes"


def obtener_conexion() -> pyodbc.Connection:
    """
    Devuelve una conexión a SQL Server usando autenticación integrada
    de Windows (Trusted_Connection=yes).
    """
    print("\n" + "="*25 + " OBTENIENDO CONEXIÓN " + "="*25)
    # Mostrar drivers ODBC disponibles en el sistema
    try:
        available_drivers = pyodbc.drivers()
        print("[INFO] Drivers ODBC detectados en el sistema:")
        for drv in available_drivers:
            print(f"    - {drv}")
    except Exception as e:
        print(f"[!] No se pudo obtener la lista de drivers ODBC. Error: {e}")
    for driver in _DRIVERS:
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={_SERVER};"
            f"DATABASE={_DATABASE};"
            "Trusted_Connection=yes;"
        )
        try:
            print(f"[*] Intentando conectar con driver: '{driver}'...")
            conn = pyodbc.connect(conn_str, timeout=5)
            print(f"[+] Conexión exitosa con '{driver}'.")
            print("="*72 + "\n")
            return conn
        except pyodbc.Error as e:
            # Prueba con el siguiente driver
            print(f"[!] Falló la conexión con '{driver}'. Error: {e}")
            continue

    print("[X]"*24)
    print("!!! NO SE PUDO ESTABLECER CONEXIÓN CON SQL SERVER !!!")
    print("[X]"*24 + "\n")
    raise ConnectionError(
        "❌ No se pudo establecer conexión con SQL Server. "
        "Verifica drivers instalados y credenciales."
    )
