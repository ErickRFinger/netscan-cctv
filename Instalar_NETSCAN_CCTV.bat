@echo off
setlocal
cd /d "%~dp0"
title Instalador NETSCAN CCTV PRO
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer.ps1"
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Deseja iniciar o NETSCAN CCTV agora? (S/N)
    set /p choice=
    if /i "%choice%"=="S" (
        start "" "%LOCALAPPDATA%\Programs\NETSCAN_CCTV\NETSCAN_CCTV.exe"
    )
) else (
    echo [ERRO] Ocorreu uma falha na instalacao.
    pause
)
