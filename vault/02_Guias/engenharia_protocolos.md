---
tipo: guide
tags:
  - guia
  - cctv
  - engenharia-reversa
  - protocolos
---

# Guia de Engenharia Reversa dos Protocolos CFTV

Detalhamento técnico dos protocolos proprietários e abertos de CFTV suportados.

## 1. Hikvision (SADP)
- **Porta:** UDP `37020`.
- **Destino:** Multicast `239.255.255.250` e Broadcast `255.255.255.255`.
- **Formato:** XML com tags `<Probe>`, `<ProbeMatch>`, `<SetDeviceParam>` e `<Activate>`.

## 2. Uniview (EZTools & LAPI)
- **Portas:** UDP `3702` (ONVIF WS-Discovery) e UDP `37020` / `12345` (EZTools).
- **Formato:** JSON `ModifyNetworkParam` e HTTP PUT REST `/LAPI/V1.0/System/Network/Interfaces/1/IPv4`.

## 3. Intelbras & Dahua (DHDiscover)
- **Porta:** UDP `37810`.
- **Formato:** JSON com `client.search` e `client.modifyIP`.

## Links Relacionados
- [[00_Core/protocolos|Especificação dos Protocolos]]
- [[01_Modulos/discovery|Motor de Descoberta]]
- [[_Index|Índice dos Guias]]
