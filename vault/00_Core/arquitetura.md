---
tipo: reference
tags:
  - arquitetura
  - backend
  - aiohttp
---

# Arquitetura do NETSCAN CCTV

## Visão Geral
O sistema opera como um aplicativo híbrido desktop-web:
1. **Engine de Rede (`core/`):** Utiliza sockets UDP puros com `SO_BROADCAST`, `SO_REUSEADDR` e `IP_ADD_MEMBERSHIP` para envio e escuta simultânea nas placas físicas.
2. **Servidor Local (`server.py`):** Roda em Python assíncrono (`aiohttp.web`) na porta `37021`.
3. **Janela Nativa Desktop (`app.py`):** Encapsula a aplicação em janela nativa de alta performance via `pywebview` (Edge WebView2) e compilação em executável único `.exe` com PyInstaller.
4. **Interface Visual (`public/index.html`):** Single-Page Application construída com Tailwind CSS e FontAwesome. Pode ser acessada no aplicativo nativo de PC ou no Safari de qualquer celular na mesma rede local via QR Code.
