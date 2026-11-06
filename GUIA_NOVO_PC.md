# 🚀 Guia de Continuação em Novo PC — NETSCAN CCTV PRO

Este documento contém todas as orientações para copiar esta pasta, abrir em qualquer outro computador e **continuar o projeto imediatamente**, seja para uso em campo ou para continuar programando com IAs (Antigravity, Cline, Claude Code, Cursor, VS Code).

---

## 📂 Opções para Levar ao Novo PC

### Opção 1: Copiar a Pasta Completa (Pendrive / HD Externo / Tailscale)
Copie a pasta inteira `NETSCAN_CCTV` para o novo computador (ex: na Área de Trabalho ou `C:\Projetos\NETSCAN_CCTV`).
> **Dica:** O executável já compilado (`dist/NETSCAN_CCTV.exe`), todo o código-fonte, interface e vault de documentação irão juntos!

### Opção 2: Clonar via Git (GitHub)
Se o novo PC tiver Git instalado, basta rodar no terminal:
```bash
git clone https://github.com/ErickRFinger/netscan-cctv.git
cd netscan-cctv
```

---

## 🛠️ Cenário A: Quero Apenas USAR no Novo PC (Sem Programar)

Você **não precisa de Python, nem de internet, nem de instalar nada**:
1. Abra a pasta `NETSCAN_CCTV`.
2. Para instalar no Windows com atalhos na Área de Trabalho e Menu Iniciar:
   - Dê um duplo clique em **`Instalar_NETSCAN_CCTV.bat`**.
3. Ou, se preferir modo portátil (sem instalar):
   - Entre na subpasta `dist/` e execute direto o **`NETSCAN_CCTV.exe`**.

---

## 💻 Cenário B: Quero CONTINUAR PROGRAMANDO no Novo PC

### 1. Pré-requisitos
- **Windows 10 ou 11** (com Edge WebView2, já presente de fábrica).
- **Python 3.10 ou superior** instalado.  
  *(Ao instalar o Python, lembre-se de marcar a caixa **"Add python.exe to PATH"**).*

### 2. Configurar o Ambiente com 1 Clique
Dê um duplo clique no arquivo:
👉 **`setup_ambiente.bat`**

Ele atualizará o `pip` e instalará automaticamente todas as dependências listadas em `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Rodar em Modo Desenvolvimento
Abra o terminal na pasta e execute:
```bash
# Inicia servidor assíncrono + janela nativa do app
python app.py

# Ou, se quiser rodar apenas o servidor web (porta 37021):
python server.py --open
```

### 4. Como Recompilar um Novo Executável (.exe)
Após fazer alterações no código ou na interface HTML:
1. Dê um duplo clique em **`build.bat`**.
2. O script executará o PyInstaller com todas as flags necessárias (`--noconsole`, `--onefile`, ícones e ativos embutidos).
3. O novo executável atualizado será gerado automaticamente em **`dist/NETSCAN_CCTV.exe`**.

---

## 🤖 Cenário C: Como Fazer Outra IA Continuar o Projeto

Se você abrir este projeto em outra máquina usando **Antigravity**, **Cline**, **Claude Code**, **Cursor** ou **Copilot**, a IA saberá exatamente o que fazer porque os contratos de memória já estão configurados:

1. **Arquivos de Gatilho de IA Presentes:**
   - `CLAUDE.md`: Instruções para Claude Code / Anthropic.
   - `GEMINI.md`: Instruções para Antigravity IDE e Gemini.
   - `AGENTS.md`: Instruções genéricas para qualquer agente autônomo.
   - `.clinerules`: Instruções para a extensão Cline no VS Code.

2. **O "Segundo Cérebro" Persistente (`vault/`):**
   - Toda a arquitetura e engenharia reversa estão documentadas na pasta [`vault/`](vault/) no padrão **VAULT-STANDARD (Obsidian)**.
   - Peça para a nova IA:  
     *"Leia o `vault/_Index.md` e o `vault/Agente.md` para carregar o contexto do projeto antes de começar."*
   - A IA lerá os módulos, os protocolos e os logs de sessão, mantendo a continuidade perfeita sem perder nada do que já foi feito.

---

## 📁 Estrutura de Arquivos da Pasta

```
NETSCAN_CCTV/
├── app.py                      # Entrypoint desktop (inicia aiohttp + pywebview)
├── server.py                   # Servidor assíncrono REST API (porta 37021)
├── build.bat                   # Script de 1 clique para compilar o .exe
├── setup_ambiente.bat          # Script de 1 clique para configurar dependências
├── requirements.txt            # Lista de dependências Python
├── icon.ico                    # Ícone oficial de câmera CFTV em alta definição
├── create_icon.py              # Script gerador do arquivo .ico
├── Instalar_NETSCAN_CCTV.bat   # Instalador oficial para o Windows
├── installer.ps1               # Script PowerShell de instalação e atalhos
├── launch.bat / abrir.vbs      # Inicializadores rápidos silenciosos
├── README.md                   # Apresentação do projeto e comandos
├── GUIA_NOVO_PC.md             # Este guia passo a passo
│
├── core/                       # Motores de Protocolo de Rede (Python)
│   ├── discovery.py            # Motor multi-socket concorrente e unificador
│   ├── network.py              # Detecção oculta de placas físicas e IPs
│   ├── hikvision.py            # Protocolo SADP (UDP 37020), ativação e alteração
│   ├── uniview.py              # Protocolo EZTools (UDP 37020/12345) e LAPI REST
│   ├── dahua.py                # Protocolo DHDiscover Intelbras/Dahua (UDP 37810)
│   └── onvif.py                # Protocolo padrão ONVIF WS-Discovery (UDP 3702)
│
├── public/                     # Interface Web 100% Offline (Single-Page App)
│   ├── index.html              # Interface estilo Black Obsidian & Cyan Glow
│   ├── tailwind.js             # Compilador local Tailwind CSS (sem internet)
│   ├── fontawesome.js          # Ícones vetoriais SVG locais (sem internet)
│   └── qrcode.js               # Gerador de QR Code local para iPhone/Android
│
├── dist/                       # Executável Final Standalone
│   └── NETSCAN_CCTV.exe        # Aplicativo portátil pronto para uso (~16.7 MB)
│
└── vault/                      # Segundo Cérebro Persistente (Modelo Obsidian)
    ├── _Index.md               # Mapa-mestre de navegação
    ├── Agente.md               # Contrato de manutenção para IAs
    ├── 00_Core/                # Protocolos e arquitetura compartilhada
    ├── 01_Modulos/             # Notas atômicas de cada componente de código
    ├── 02_Guias/               # Guias passo a passo e engenharia reversa
    └── _Logs/                  # Histórico auditável de sessões
```

---

## 🌐 Links Externos Oficiais
- **Repositório GitHub:** [github.com/ErickRFinger/netscan-cctv](https://github.com/ErickRFinger/netscan-cctv)
- **Download do Executável v1.0.0:** [GitHub Releases](https://github.com/ErickRFinger/netscan-cctv/releases/tag/v1.0.0)
