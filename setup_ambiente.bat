@echo off
setlocal
cd /d "%~dp0"
title NETSCAN CCTV — Configurador de Ambiente para Novo PC

echo ========================================================
echo   NETSCAN CCTV PRO — SETUP AUTOMATICO DE AMBIENTE
echo ========================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Python nao foi encontrado no PATH do sistema.
    echo Por favor, instale o Python 3.10+ marcando a opcao "Add python.exe to PATH".
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] Python detectado:
python --version
echo.

echo [2/3] Instalando dependencias de requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias via pip.
    pause
    exit /b 1
)

echo.
echo [3/3] Ambiente configurado com sucesso!
echo.
echo ========================================================
echo   COMO INICIAR O PROJETO NESTE PC:
echo.
echo   1. Rodar em modo Desenvolvimento:
echo      python app.py
echo.
echo   2. Rodar o executavel pronto (sem precisar de nada):
echo      dist\NETSCAN_CCTV.exe
echo.
echo   3. Instalar no Windows com atalhos:
echo      Instalar_NETSCAN_CCTV.bat
echo.
echo   4. Recompilar o .exe apos modificacoes:
echo      build.bat
echo ========================================================
echo.
pause
