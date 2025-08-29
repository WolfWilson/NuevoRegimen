# 🏛️ Gestión de Régimen con PyQt5 y SQL Server

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-6.x-green.svg)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-orange.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

Este proyecto es una aplicación de escritorio desarrollada en **Python** con **PyQt5**, que permite gestionar el **régimen previsional** de personas mediante un número de **CUIL**, obteniendo y modificando su información en una base de datos **SQL Server**.

## 🚀 Características

✅ **Búsqueda de datos personales**: Consultar nombre y fecha de nacimiento de una persona por su CUIL.  
✅ **Consulta del régimen actual**: Ver el régimen asignado a la persona en la base de datos.  
✅ **Actualización del régimen**: Modificar el régimen de la persona desde la interfaz.  
✅ **Interfaz moderna**: Diseño con **PyQt5** y estilos personalizados en `Modules/style.py`.  
✅ **Conexión segura a SQL Server** con `pyodbc`.

---

## 🛠️ Instalación y Configuración

### 1️⃣ **Clonar el repositorio**
```sh
git clone https://github.com/tu_usuario/NuevoRegimen.git
cd NuevoRegimen
```

### 2️⃣ Crear un entorno virtual y activarlo
```sh
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

### 3️⃣ Instalar dependencias
```sh
pip install -r requirements.txt

```

### 4️⃣ Configurar la conexión a SQL Server
```sh
server = 'PC-2193'  # Nombre del servidor
database = 'Aportes'  # Nombre de la base de datos


```

### 5️⃣ Ejecutar la aplicación
```sh
python main.py
```

## 📸 Captura de Pantalla

[![imagen-2025-03-11-110330270.png](https://i.postimg.cc/6pNdqkrr/imagen-2025-03-11-110330270.png)](https://postimg.cc/ykvJrrrx)

## 🖥️ Estructura del Proyecto
```sh
NuevoRegimen/
│── Modules/
│   ├── style.py   # Estilos y personalización de la interfaz
│── main.py        # Lógica principal de la aplicación
│── requirements.txt  # Dependencias del proyecto
│── README.md      # Documentación del proyecto
```
## 🖥️ Pyinstaller
```sh
# 1. Compilar el ejecutable con PyInstaller
pyinstaller main.py --onefile --noconsole --icon=Source/icon.ico --add-data "Source;Source" --add-data "Modules/resources.py;Modules" --add-data "Modules/style.py;Modules" --add-data "Modules/conexion_db.py;Modules" --name GestorRegimen

# 2. Copiar el ejecutable generado a la carpeta de red, sobrescribiendo si existe
Copy-Item -Path ".\\dist\\GestorRegimen.exe" -Destination "\\\\fs01\\ExeGSP\\GestorRegimen.exe" -Force
```

## 🗃️ Procedimientos Almacenados en SQL Server
```sh
📌 Anto_ObtenerPersonaPorCUIL
CREATE PROCEDURE Anto_ObtenerPersonaPorCUIL
    @CUIL VARCHAR(11)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT Apeynom, Fec_nac
    FROM Personas
    WHERE CUIL = @CUIL;
END;
```

📌 anto_regimenactual
```sh
CREATE PROCEDURE anto_regimenactual
    @CUIL VARCHAR(11)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT REGIMEN
    FROM [Aportes].[dbo].[WS_SELECCION_REGIMEN]
    WHERE CUIL = @CUIL;
END;
```

📌 Anto_CambiarRegimen
```sh
CREATE PROCEDURE Anto_CambiarRegimen
    @CUIL VARCHAR(11),
    @NuevoRegimen INT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE [Aportes].[dbo].[WS_SELECCION_REGIMEN]
    SET REGIMEN = @NuevoRegimen
    WHERE CUIL = @CUIL;
END;
```

### 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si deseas mejorar el proyecto:

Haz un fork 🍴
Crea una rama (git checkout -b feature-nueva)
Realiza tus cambios y commitea (git commit -m "Nueva funcionalidad")
Envía un Pull Request ✅

### 📜 Licencia
Este proyecto está bajo la licencia MIT.

### 💡 Desarrollado con ❤️ por Anto



