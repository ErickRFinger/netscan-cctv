---
tipo: guide
tags:
  - guia
  - onboarding
  - setup
  - portabilidade
---

# Guia de Configuração em Novo Computador

Instruções para inicializar o ambiente de desenvolvimento do NETSCAN CCTV em qualquer máquina.

## Pré-requisitos
- Windows 10/11 com motor Edge WebView2.
- Python 3.10 ou superior adicionado ao PATH.

## Passos de Inicialização
1. **Configuração Automática:**
   Executar `setup_ambiente.bat` ou rodar no terminal:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execução em Desenvolvimento:**
   ```bash
   python app.py
   ```
3. **Execução do Executável Pronto:**
   Executar `dist/NETSCAN_CCTV.exe` sem precisar de Python.

## Links Relacionados
- [[00_Core/arquitetura|Arquitetura do Sistema]]
- [[compilacao_distribuicao|Guia de Compilação]]
- [[_Index|Índice dos Guias]]
