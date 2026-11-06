# NETSCAN CCTV — SADP & EZTools Universal

Ferramenta desktop e móvel unificada para técnicos de CFTV e segurança eletrônica.
Substitui a necessidade de rodar SADP (Hikvision), EZTools (Uniview) e ConfigTool (Intelbras/Dahua) separadamente.

---

## ⚡ Recursos Principais
- **Descoberta Multi-Protocolo L2/L3:** Varre e detecta câmeras mesmo com IPs fora da faixa da rede local.
- **Hikvision (SADP):** Descoberta, alteração de parâmetros de rede e ativação de câmeras inativas.
- **Uniview (EZTools / LAPI):** Descoberta proprietária UNV e suporte ONVIF WS-Discovery.
- **Intelbras / Dahua:** Descoberta automática via DHDiscover (UDP 37810).
- **Sequenciamento em Lote:** Defina um IP inicial e numere todas as câmeras selecionadas em 1 clique.
- **Modo Aplicativo Nativo:** Inicia no Windows como janela isolada de app sem barras do navegador.
- **Acesso pelo Celular (iPhone / Android):** Gere o QR Code na tela do notebook; o técnico aponta a câmera do celular e controla tudo pelo navegador do smartphone conectado no mesmo Wi-Fi.

---

## 🚀 Como Iniciar e Instalar
- **Opção 1 (Instalação no Windows):** Dê um duplo clique em `Instalar_NETSCAN_CCTV.bat`. Ele criará o atalho com ícone na **Área de Trabalho** e no **Menu Iniciar**.
- **Opção 2 (Executável Standalone Portátil):** Execute direto `dist/NETSCAN_CCTV.exe` (pode colocar num pendrive, não precisa de Python).
- **Opção 3 (Atalho Rápido na Área de Trabalho):** Dê um duplo clique em `NETSCAN CCTV` direto no Desktop.
- **Opção 4 (Ambiente de Desenvolvimento):** Execute `setup_ambiente.bat` e rode `python app.py`.

---

## 💻 Levando o Projeto para Outro Computador
Para abrir e continuar o desenvolvimento ou uso em outra máquina, consulte o guia passo a passo completo:
👉 **[`GUIA_NOVO_PC.md`](GUIA_NOVO_PC.md)**

1. Dê um duplo clique em **`setup_ambiente.bat`** para instalar todas as dependências do `requirements.txt`.
2. Execute **`python app.py`** para rodar em modo de desenvolvimento.
3. Execute **`build.bat`** sempre que quiser compilar um novo executável atualizado em `dist/`.

---

## 📚 Documentação (Padrão Obsidian)
O projeto mantém documentação atômica e segundo cérebro persistente em [`vault/`](vault/):
- Mapa-mestre: [`vault/_Index.md`](vault/_Index.md)
- Contrato do agente: [`vault/Agente.md`](vault/Agente.md)
- Guias práticos: [`vault/02_Guias/_Index.md`](vault/02_Guias/_Index.md)
- Repositório oficial: [github.com/ErickRFinger/netscan-cctv](https://github.com/ErickRFinger/netscan-cctv)
