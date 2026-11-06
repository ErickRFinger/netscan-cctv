"""
NETSCAN CCTV PRO — Desktop Application Launcher
Inicializa o servidor de varredura UDP em segundo plano e abre a janela nativa do aplicativo.
"""

import os
import sys

# Redirecionamento seguro para PyInstaller --noconsole
log_dir = os.environ.get("LOCALAPPDATA", os.path.dirname(os.path.abspath(__file__)))
log_path = os.path.join(log_dir, "netscan_boot.log")

class SafeWriter:
    def __init__(self, filename):
        self.filename = filename
    def write(self, s):
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(str(s))
        except Exception:
            pass
    def flush(self):
        pass

if sys.stdout is None:
    sys.stdout = SafeWriter(log_path)
if sys.stderr is None:
    sys.stderr = SafeWriter(log_path)

import time
import socket
import threading
import asyncio

# Suporte ao empacotamento com PyInstaller
if getattr(sys, "frozen", False):
    BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

from aiohttp import web
from server import make_app
import webview

PORT = 37021

def is_port_in_use(port=PORT):
    """Verifica se o servidor já está ativo na porta."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.4)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False

def start_background_server(port=PORT):
    """Inicia o servidor aiohttp em thread assíncrona desacoplada."""
    def run():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            app = make_app()
            runner = web.AppRunner(app)
            loop.run_until_complete(runner.setup())
            site = web.TCPSite(runner, "0.0.0.0", port)
            loop.run_until_complete(site.start())
            print(f"[NETSCAN CCTV] Servidor local ativo em http://127.0.0.1:{port}")
            loop.run_forever()
        except Exception as e:
            print(f"[NETSCAN CCTV] Erro no servidor: {e}")

    t = threading.Thread(target=run, daemon=True)
    t.start()
    
    # Aguarda o servidor responder
    for _ in range(30):
        if is_port_in_use(port):
            break
        time.sleep(0.1)

def main():
    try:
        print("[NETSCAN CCTV] Iniciando aplicacao...")
        if not is_port_in_use(PORT):
            start_background_server(PORT)
        else:
            print(f"[NETSCAN CCTV] Servidor ja detectado ativo na porta {PORT}.")

        icon_path = os.path.join(BASE_DIR, "icon.ico")
        if not os.path.exists(icon_path):
            icon_path = None

        # Cria janela nativa moderna (WebView2 / Edge Chromium)
        window = webview.create_window(
            title="NETSCAN CCTV PRO — SADP & EZTools Suite",
            url=f"http://127.0.0.1:{PORT}",
            width=1440,
            height=890,
            min_size=(1050, 680),
            background_color="#080a0f",
            confirm_close=False
        )

        print("[NETSCAN CCTV] Abrindo janela grafica...")
        # Inicia loop de interface gráfica
        webview.start(debug=False)
        print("[NETSCAN CCTV] Janela fechada pelo usuario.")
    except Exception as e:
        print(f"[NETSCAN CCTV] Falha fatal: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
