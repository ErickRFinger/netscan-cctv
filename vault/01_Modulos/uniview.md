---
tipo: componente
tags:
  - uniview
  - eztools
  - onvif
---

# Módulo Uniview (`core/uniview.py` & `core/onvif.py`)

## Funcionalidades
- `build_unv_probe()`: Monta pacote JSON e probe de descoberta para o protocolo EZTools da Uniview.
- `build_onvif_probe()`: Gera o envelope SOAP WS-Discovery para a porta 3702, reconhecido nativamente por todas as câmeras Uniview.
- `parse_onvif_response()`: Extrai fabricante, modelo de hardware (`IPC...`) e URL do serviço de gerenciamento ONVIF a partir das tags `<XAddrs>` e `<Scopes>`.
