---
tipo: guide
tags:
  - guia
  - build
  - pyinstaller
  - distribuicao
---

# Guia de Compilação e Distribuição

Como gerar o executável standalone e distribuir para técnicos.

## Processo de Build
1. **Via Script de 1 Clique:**
   Executar `build.bat` na raiz do projeto.
2. **Via Comando Manual PyInstaller:**
   ```bash
   python -m PyInstaller --noconsole --onefile --icon "icon.ico" --name "NETSCAN_CCTV" --add-data "public;public" --add-data "core;core" --add-data "icon.ico;." --hidden-import aiohttp --hidden-import webview --hidden-import clr_loader --hidden-import pythonnet --clean app.py
   ```

## Cuidados na Compilação
- As flags `--noconsole` exigem que `sys.stdout` e `sys.stderr` sejam protegidos contra `NoneType`.
- Subprocessos devem utilizar `CREATE_NO_WINDOW` para evitar janelas pretas no Windows.

## Links Relacionados
- [[01_Modulos/desktop_app|Módulo Desktop App]]
- [[novo_ambiente|Guia de Novo Ambiente]]
- [[_Index|Índice dos Guias]]
