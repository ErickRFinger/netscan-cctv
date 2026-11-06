---
tipo: reference
tags:
  - protocolos
  - sadp
  - eztools
  - onvif
---

# Protocolos de Rede CFTV

Documentação técnica dos protocolos de Camada 2/3 implementados:

## 1. Hikvision SADP
- **Transporte:** UDP Multicast em `239.255.255.250:37020` e Broadcast `255.255.255.255:37020`.
- **Formato:** XML com tags `<Probe>`, `<ProbeMatch>`, `<SetDeviceParam>` e `<Activate>`.
- **Diferencial:** Permite alterar IP mesmo com a câmera em sub-rede diferente.

## 2. Uniview (EZTools) & ONVIF WS-Discovery
- **Transporte:** UDP Multicast em `239.255.255.250:3702` (WS-Discovery) e portas proprietárias `37020` / `12345`.
- **Formato:** SOAP Envelope com `<d:Probe>` para tipos `dn:NetworkVideoTransmitter`.
- **Resposta:** XAddrs contendo porta HTTP e Scopes contendo modelo e fabricante.

## 3. Intelbras / Dahua (DHDiscover)
- **Transporte:** UDP Broadcast em porta `37810`.
- **Formato:** JSON `client.search` retornando MAC, IP, máscara e gateway.
