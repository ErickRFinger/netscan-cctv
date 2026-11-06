@echo off
setlocal
cd /d "%~dp0"
echo ========================================================
echo   COMPILANDO NETSCAN CCTV PRO — EXECUTAVEL STANDALONE
echo ========================================================

python -m PyInstaller ^
    --noconsole ^
    --onefile ^
    --icon "icon.ico" ^
    --name "NETSCAN_CCTV" ^
    --add-data "public;public" ^
    --add-data "core;core" ^
    --add-data "icon.ico;." ^
    --hidden-import aiohttp ^
    --hidden-import webview ^
    --hidden-import clr_loader ^
    --hidden-import pythonnet ^
    --clean ^
    app.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCESSO] Compilacao concluida com exito!
    echo Executavel gerado em: dist\NETSCAN_CCTV.exe
) else (
    echo.
    echo [ERRO] Falha durante a compilacao.
)
pause
