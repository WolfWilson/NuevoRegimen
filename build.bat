@echo off
chcp 65001 >nul
setlocal

echo.
echo ══════════════════════════════════════════════════════
echo   BUILD  --  GestorRegimen
echo ══════════════════════════════════════════════════════
echo.

:: ── Activar entorno virtual ───────────────────────────────────────────
set "VENV=%~dp0venv\Scripts\activate.bat"
if exist "%VENV%" (
    call "%VENV%"
    echo [+] Entorno virtual activado.
) else (
    echo [!] No se encontro el entorno virtual en venv\
    echo     Asegurate de crearlo con: python -m venv venv
    pause
    exit /b 1
)

:: ── Limpiar builds anteriores ─────────────────────────────────────────
echo.
echo [*] Limpiando builds anteriores...

if exist "build\"     rmdir /s /q "build"
if exist "dist\"      rmdir /s /q "dist"
if exist "GestorRegimen.spec" del /q "GestorRegimen.spec"

echo [+] Limpieza completada.

:: ── Compilar ──────────────────────────────────────────────────────────
echo.
echo [*] Compilando con PyInstaller...
echo.

pyinstaller main.py ^
    --onedir ^
    --noconsole ^
    --clean ^
    --icon=Source/icon.ico ^
    --add-data "Source;Source" ^
    --add-data "UI;UI" ^
    --add-data "Modules/resources.py;Modules" ^
    --add-data "Modules/style.py;Modules" ^
    --add-data "Modules/conexion_db.py;Modules" ^
    --name GestorRegimen

if errorlevel 1 (
    echo.
    echo [!!!] ERROR: La compilacion fallo.
    pause
    exit /b 1
)

echo.
echo [+] Compilacion exitosa: dist\GestorRegimen.exe

:: ── Copiar a carpeta de red (sobrescribe) ─────────────────────────────
set "DESTINO=\\fs01\ExeGSP\GestorRegimen.exe"

echo.
echo [*] Copiando a %DESTINO% ...

copy /y "dist\GestorRegimen.exe" "%DESTINO%"

if errorlevel 1 (
    echo [!] No se pudo copiar al destino de red.
    echo     Verifica que \\fs01\ExeGSP sea accesible.
) else (
    echo [+] Copia exitosa en red.
)

:: ── Limpiar artefactos intermedios post-build ─────────────────────────
echo.
echo [*] Limpiando artefactos intermedios...

if exist "build\"             rmdir /s /q "build"
if exist "GestorRegimen.spec" del /q "GestorRegimen.spec"

echo [+] Hecho.

echo.
echo ══════════════════════════════════════════════════════
echo   BUILD COMPLETADO  --  dist\GestorRegimen.exe
echo ══════════════════════════════════════════════════════
echo.
pause
endlocal
