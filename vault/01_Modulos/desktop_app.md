---
tipo: module
tags:
  - desktop
  - pyinstaller
  - webview
  - instalador
---

# Módulo Desktop App & Instalador

Responsável pela experiência de aplicativo instalável nativo no Windows sem dependência de terminais ou navegadores externos.

## Componentes
- `app.py`: Entrypoint desktop que sobe o servidor aiohttp em thread daemon desacoplada e inicializa a janela WebView2 (`pywebview`).
- `icon.ico`: Ícone oficial de câmera CFTV em múltiplos tamanhos.
- `installer.ps1` e `Instalar_NETSCAN_CCTV.bat`: Criador da instalação em `%LOCALAPPDATA%\Programs\NETSCAN_CCTV\`, atalhos no Desktop e Menu Iniciar.
- `build.bat`: Script de compilação PyInstaller 6.21.0 gerando o standalone `dist/NETSCAN_CCTV.exe` (100% offline, zero dependências).
- `public/`: Contém interface com Tailwind, FontAwesome e QRCode gerados 100% offline (air-gapped).

## Links
- [[arquitetura]]
- [[discovery]]
