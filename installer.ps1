# Instalador do NETSCAN CCTV PRO
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "    INSTALADOR OFICIAL: NETSCAN CCTV PRO (SADP e EZTools) " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExeSource = Join-Path $SourceDir "dist\NETSCAN_CCTV.exe"
$IconSource = Join-Path $SourceDir "icon.ico"

if (-not (Test-Path $ExeSource)) {
    Write-Host "[ERRO] Executavel compilado nao encontrado em: $ExeSource" -ForegroundColor Red
    exit 1
}

$InstallDir = "$env:LOCALAPPDATA\Programs\NETSCAN_CCTV"
Write-Host "`n[1/4] Criando diretorio de instalacao em:" -ForegroundColor Green
Write-Host "      $InstallDir" -ForegroundColor Gray

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
}

Write-Host "[2/4] Copiando arquivos do aplicativo..." -ForegroundColor Green
Copy-Item -Path $ExeSource -Destination (Join-Path $InstallDir "NETSCAN_CCTV.exe") -Force
if (Test-Path $IconSource) {
    Copy-Item -Path $IconSource -Destination (Join-Path $InstallDir "icon.ico") -Force
}

Write-Host "[3/4] Criando atalhos no Desktop e Menu Iniciar..." -ForegroundColor Green
$WshShell = New-Object -ComObject WScript.Shell

# 1. Desktop Shortcut
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$DesktopShortcut = $WshShell.CreateShortcut((Join-Path $DesktopPath "NETSCAN CCTV.lnk"))
$DesktopShortcut.TargetPath = (Join-Path $InstallDir "NETSCAN_CCTV.exe")
$DesktopShortcut.WorkingDirectory = $InstallDir
$DesktopShortcut.Arguments = ""
$DesktopShortcut.IconLocation = "$InstallDir\icon.ico,0"
$DesktopShortcut.Description = "NETSCAN CCTV PRO - SADP e EZTools Universal"
$DesktopShortcut.Save()

# 2. Start Menu Shortcut
$StartPrograms = [Environment]::GetFolderPath("Programs")
$StartAppDir = Join-Path $StartPrograms "NETSCAN CCTV"
if (-not (Test-Path $StartAppDir)) {
    New-Item -ItemType Directory -Force -Path $StartAppDir | Out-Null
}
$StartShortcut = $WshShell.CreateShortcut((Join-Path $StartAppDir "NETSCAN CCTV.lnk"))
$StartShortcut.TargetPath = (Join-Path $InstallDir "NETSCAN_CCTV.exe")
$StartShortcut.WorkingDirectory = $InstallDir
$StartShortcut.Arguments = ""
$StartShortcut.IconLocation = "$InstallDir\icon.ico,0"
$StartShortcut.Description = "NETSCAN CCTV PRO - SADP e EZTools Universal"
$StartShortcut.Save()

# 3. Uninstaller Script
$UninstallScript = @"
@echo off
title Desinstalador - NETSCAN CCTV PRO
echo Removendo NETSCAN CCTV PRO...
taskkill /f /im NETSCAN_CCTV.exe >nul 2>&1
del /f /q "$DesktopPath\NETSCAN CCTV.lnk" >nul 2>&1
rmdir /s /q "$StartAppDir" >nul 2>&1
echo Atalhos removidos com sucesso.
echo Para remover os arquivos completamente, exclua a pasta:
echo "$InstallDir"
pause
"@
Set-Content -Path (Join-Path $InstallDir "Desinstalar.bat") -Value $UninstallScript -Encoding ASCII

# Desinstalador no Menu Iniciar
$UninstallShortcut = $WshShell.CreateShortcut((Join-Path $StartAppDir "Desinstalar NETSCAN CCTV.lnk"))
$UninstallShortcut.TargetPath = (Join-Path $InstallDir "Desinstalar.bat")
$UninstallShortcut.WorkingDirectory = $InstallDir
$UninstallShortcut.Save()

Write-Host "[4/4] Instalacao Concluida com Sucesso!" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " Atalho criado na sua Area de Trabalho: NETSCAN CCTV" -ForegroundColor Yellow
Write-Host " Aplicativo cadastrado no Menu Iniciar do Windows" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
