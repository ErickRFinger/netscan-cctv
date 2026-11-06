---
tipo: componente
tags:
  - hikvision
  - sadp
---

# Módulo Hikvision (`core/hikvision.py`)

## Funcionalidades
- `build_sadp_probe()`: Monta pacote XML de inquiry com UUID único.
- `parse_sadp_response()`: Extrai dados como número de série, MAC, versão de firmware, porta HTTP e se a câmera já está ativada.
- `build_sadp_modify_xml()`: Permite enviar parâmetros de novo IP, máscara e gateway assinados com a senha de administrador da câmera.
- `build_sadp_activate_xml()`: Permite definir a senha mestre inicial em câmeras recém-instaladas.
