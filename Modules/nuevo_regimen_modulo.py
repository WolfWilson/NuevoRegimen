import pyodbc
from datetime import datetime

drivers = [
        'ODBC Driver 17 for SQL Server',  # Preferido y más reciente
        'SQL Server Native Client 11.0',  # Native Client version 11
        'SQL Server Native Client 10.0',  # Native Client version 10
        'SQL Server',  # Generic ODBC driver name (legacy)
    ]

def obtener_conexion():
    # Configura la conexión a la base de datos SQL Server.
    server = 'sql01'
    database = 'Aportes'

    for driver in drivers:
        conexion_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
        try:
            print(f"Intentando conectar con el driver: {driver}")
            conexion = pyodbc.connect(conexion_str)
            print(f"Conexión exitosa con el driver: {driver}")
            return conexion
        except pyodbc.Error as error:
            print(f"Error al intentar conectar con el driver: {driver}")
            print(error)
    
    raise Exception("No se pudo conectar a la base de datos con ninguno de los drivers disponibles.")