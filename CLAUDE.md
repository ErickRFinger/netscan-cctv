# Instruções para Claude / Agentes de IA — NETSCAN CCTV

Este projeto é uma ferramenta unificada de engenharia reversa para CFTV (SADP Hikvision + EZTools Uniview + DHDiscover Intelbras/Dahua), contendo documentação estruturada no padrão Obsidian em [`vault/`](vault/).

## 🧠 Ordem Obrigatória de Leitura de Memória (VAULT-STANDARD)
Antes de modificar qualquer código, leia o contexto nesta ordem:
1. [`vault/_Index.md`](vault/_Index.md) — mapa-mestre de navegação.
2. `vault/01_Modulos/_Overview.md` — visão geral e responsabilidade dos módulos.
3. Notas atômicas específicas do que vai alterar (`discovery.md`, `hikvision.md`, `uniview.md`, `desktop_app.md`).
4. `vault/00_Core/` — protocolos de rede CFTV (UDP Multicast/Broadcast) e arquitetura assíncrona.
5. Logs recentes em `vault/_Logs/`.

## 🛠️ Regras de Desenvolvimento:
- **Backend:** Python assíncrono com `aiohttp` rodando na porta `37021`.
- **Janela Desktop:** `pywebview` usando motor Edge WebView2 nativo no Windows.
- **Execução Oculta:** Toda invocação de sistema deve usar `creationflags=subprocess.CREATE_NO_WINDOW` e `SW_HIDE` para evitar consoles pretos na tela.
- **Frontend:** Single-Page Application em `public/index.html` 100% offline (Tailwind, FontAwesome SVG e QRCode locais embutidos).
- **Compilação:** Standalone com PyInstaller via `build.bat` gerando `dist/NETSCAN_CCTV.exe`.

## 📋 Checklist Obrigatório de Saída ao Finalizar:
- [ ] Atualizar ou criar log de sessão em `vault/_Logs/DD-MM-AAAA_<git_user_name>.md`.
- [ ] Atualizar notas atômicas afetadas (< 80 linhas, 1 conceito por nota, frontmatter YAML).
- [ ] Atualizar `vault/_Index.md` se criou nova unidade ou módulo.
- [ ] Inserir `[[wikilinks]]` nas notas modificadas/criadas.
- [ ] Recompilar o binário com `build.bat` se houver alteração de código.
