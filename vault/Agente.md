---
tipo: index
tags:
  - contrato
  - agente
  - memoria
---

# Agente.md — Contrato de Memória do Vault (NETSCAN CCTV)

> Este vault é o segundo cérebro do projeto **NETSCAN CCTV**. Objetivo: economia de tokens e contexto máximo via notas atômicas interligadas por `[[wikilinks]]`.

## Ordem Obrigatória de Leitura ao Iniciar
1. `vault/_Index.md` (mapa-mestre)
2. `_Overview.md` da unidade afetada em `01_Modulos/`
3. Notas atômicas específicas
4. `00_Core/` para protocolos ou arquitetura
5. Logs recentes em `_Logs/`

## Regras de Manutenção
- **1 nota = 1 conceito** (< 80 linhas).
- **Frontmatter YAML obrigatório** (`tipo:`, `tags:`).
- **Log obrigatório de sessão** em `_Logs/DD-MM-AAAA_<git_user_name>.md` ao finalizar alterações.
- **Linkar, não duplicar:** código-fonte e especificações canônicas são linkados, nunca clonados na íntegra.
