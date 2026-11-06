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
- **Opção 2 (Executável Standalone Portátil):** Execute direto `dist/NETSCAN_CCTV.exe` (pode colocar num pendrive).
- **Opção 3 (Atalho Rápido na Área de Trabalho):** Dê um duplo clique em `NETSCAN CCTV` direto no Desktop.
- **Opção 4 (Script de Desenvolvimento):** Execute `launch.bat`.

---

## 📚 Documentação (Padrão Obsidian)
O projeto mantém documentação atômica em [`vault/`](vault/):
- Mapa-mestre: [`vault/_Index.md`](vault/_Index.md)
- Contrato do agente: [`vault/Agente.md`](vault/Agente.md)
