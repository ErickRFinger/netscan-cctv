---
tipo: overview
tags:
  - modulos
  - overview
---

# Visão Geral dos Módulos

Os módulos em `core/` são organizados de forma desacoplada:
- `network.py`: Descobre placas de rede via PowerShell / sockets e calcula sub-redes.
- `discovery.py`: Orquestra o envio concorrente em múltiplas placas de rede e multiplexa as respostas com `select()`.
- `hikvision.py`: Monta os pacotes XML SADP e executa comandos de alteração de IP e ativação.
- `uniview.py` & `onvif.py`: Processam descoberta e metadados de câmeras Uniview e padrão ONVIF.
- `dahua.py`: Suporta DVRs/Câmeras Intelbras via DHDiscover.
