---
tipo: componente
tags:
  - discovery
  - sockets
---

# Módulo de Descoberta (`core/discovery.py`)

## Responsabilidades
- Gerencia o ciclo de vida da varredura em segundo plano.
- Para cada interface de rede ativa:
  1. Cria sockets UDP nas portas `37020`, `3702` e `37810`.
  2. Injeta associação ao grupo de multicast `239.255.255.250`.
  3. Envia simultaneamente probes SADP, ONVIF, EZTools e DHDiscover.
- Utiliza `select.select()` com timeout para capturar respostas assíncronas.
- Normaliza os dados para o formato comum `{ id, brand, model, mac, ip, mask, gateway, port, activated }`.
