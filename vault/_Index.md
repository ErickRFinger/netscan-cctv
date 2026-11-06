---
tipo: index
tags:
  - mapa-mestre
  - cctv
  - redes
---

# NETSCAN CCTV — Mapa-Mestre da Documentação

> Segundo cérebro persistente do projeto **NETSCAN CCTV** no padrão [[VAULT-STANDARD]].

## Estrutura do Vault
- [[Agente]]: O contrato de manutenção e regras de memória.
- [[00_Core/_Index|00_Core]]: Conhecimento compartilhado, arquitetura e protocolos de CFTV.
  - [[00_Core/protocolos|Protocolos de CFTV]] (SADP, EZTools, ONVIF, DHDiscover).
  - [[00_Core/arquitetura|Arquitetura do Sistema]] (Sockets assíncronos e aiohttp).
- [[01_Modulos/_Index|01_Modulos]]: Unidades e implementações do sistema.
  - [[01_Modulos/_Overview|Visão Geral dos Módulos]].
  - [[01_Modulos/discovery|Motor de Descoberta Multi-Socket]].
  - [[01_Modulos/hikvision|Módulo SADP (Hikvision)]].
  - [[01_Modulos/uniview|Módulo EZTools (Uniview)]].
  - [[01_Modulos/desktop_app|Módulo Desktop App & Instalador]].
- [[02_Guias/_Index|02_Guias]]: Guias práticos, onboarding e engenharia reversa.
  - [[02_Guias/novo_ambiente|Guia de Configuração em Novo PC]].
  - [[02_Guias/compilacao_distribuicao|Guia de Compilação do Executável]].
  - [[02_Guias/engenharia_protocolos|Engenharia Reversa dos Protocolos CFTV]].
- [[_Logs/05-11-2026_ErickFinger|Log 05/11/2026]] / [[_Logs/06-11-2026_ErickFinger|Log 06/11/2026]]: Histórico auditável de alterações.
