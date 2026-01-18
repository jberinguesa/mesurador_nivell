@echo off
REM Sistema d'Adquisició de Nivell d'Aigua - UdG
REM Executar amb doble clic

echo ========================================
echo Sistema d'Adquisicio de Nivell d'Aigua
echo Universitat de Girona
echo ========================================
echo.
echo Iniciant aplicacio...
echo.

REM Canviar al directori on està el script
cd /d "%~dp0"

REM Executar amb uv
uv run python main.py

REM Si hi ha error, mantenir finestra oberta
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: L'aplicacio no s'ha pogut iniciar
    echo ========================================
    echo.
    pause
)
