"""
Servidor Web e API REST para o NETSCAN CCTV.
Disponibiliza interface moderna para PC e dispositivos móveis na rede local.
"""

import os
import sys
import json
import asyncio
import subprocess
from aiohttp import web

# Suporte a PyInstaller e diretórios locais
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

from core.network import get_interfaces
from core.discovery import engine

PUBLIC_DIR = os.path.join(BASE_DIR, "public")

async def handle_index(request):
    """Serve a Single-Page Application."""
    index_file = os.path.join(PUBLIC_DIR, "index.html")
    if os.path.exists(index_file):
        return web.FileResponse(index_file)
    return web.Response(text="index.html não encontrado", status=404)

async def handle_get_interfaces(request):
    """Retorna placas de rede disponíveis."""
    loop = asyncio.get_event_loop()
    ifaces = await loop.run_in_executor(None, get_interfaces)
    return web.json_response({"interfaces": ifaces})

async def handle_scan(request):
    """Dispara varredura nas interfaces."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    
    interface_ip = body.get("interface_ip")
    timeout = float(body.get("timeout", 2.5))

    loop = asyncio.get_event_loop()
    devices = await loop.run_in_executor(None, engine.scan, interface_ip, timeout)
    return web.json_response({
        "success": True,
        "count": len(devices),
        "devices": devices
    })

async def handle_demo_devices(request):
    """Carrega dispositivos virtuais para demonstração e teste de bancada da UI."""
    demo_list = [
        {
            "id": "BC:54:36:A1:4F:10",
            "brand": "Hikvision",
            "model": "DS-2CD2043G2-I (4MP AcuSense)",
            "serial": "DS-2CD2043G2-I20230815AAWR123456789",
            "mac": "BC:54:36:A1:4F:10",
            "ip": "192.168.0.64",
            "mask": "255.255.255.0",
            "gateway": "192.168.0.1",
            "port": 80,
            "version": "V5.7.12 build 230720",
            "activated": True,
            "dhcp": False,
            "protocol": "SADP (Hikvision)",
            "vendor_icon": "hikvision"
        },
        {
            "id": "BC:54:36:C8:11:82",
            "brand": "Hikvision",
            "model": "DS-2CD1023G0E-I (2MP Bullet)",
            "serial": "DS-2CD1023G0E-I20240110BBR987654321",
            "mac": "BC:54:36:C8:11:82",
            "ip": "192.168.0.64",
            "mask": "255.255.255.0",
            "gateway": "192.168.0.1",
            "port": 80,
            "version": "V5.5.120 build 231105",
            "activated": False,
            "dhcp": False,
            "protocol": "SADP (Hikvision)",
            "vendor_icon": "hikvision"
        },
        {
            "id": "48:EA:63:29:8C:F4",
            "brand": "Uniview",
            "model": "IPC2124SR3-DPF40 (4MP Prime)",
            "serial": "210235C3Y53218000412",
            "mac": "48:EA:63:29:8C:F4",
            "ip": "192.168.0.120",
            "mask": "255.255.255.0",
            "gateway": "192.168.0.1",
            "port": 80,
            "version": "B3821P15D2203",
            "activated": True,
            "dhcp": True,
            "protocol": "EZTools (Uniview)",
            "vendor_icon": "uniview"
        },
        {
            "id": "3C:EF:8C:55:01:A9",
            "brand": "Intelbras",
            "model": "VIP 3230 B (2MP G4 IR 30m)",
            "serial": "PAA3LA0123456",
            "mac": "3C:EF:8C:55:01:A9",
            "ip": "192.168.0.135",
            "mask": "255.255.255.0",
            "gateway": "192.168.0.1",
            "port": 80,
            "version": "2.800.00IB001.0.R",
            "activated": True,
            "dhcp": False,
            "protocol": "DHDiscover (Intelbras)",
            "vendor_icon": "intelbras"
        }
    ]
    for d in demo_list:
        engine.devices[d["id"]] = d
    return web.json_response({"success": True, "devices": list(engine.devices.values())})

async def handle_clear_devices(request):
    """Limpa a lista de dispositivos em memória."""
    engine.devices.clear()
    return web.json_response({"success": True, "count": 0})

async def handle_get_devices(request):
    """Retorna dispositivos em memória."""
    devices = list(engine.devices.values())
    return web.json_response({
        "devices": devices,
        "scanning": engine.is_scanning
    })

async def handle_modify_device(request):
    """Altera parâmetros de rede de um dispositivo."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"success": False, "error": "JSON inválido"}, status=400)

    device_sn = data.get("serial", "")
    mac = data.get("mac", "")
    brand = data.get("brand", "")
    new_ip = data.get("new_ip", "")
    new_mask = data.get("new_mask", "255.255.255.0")
    new_gateway = data.get("new_gateway", "")
    new_port = int(data.get("new_port", 80))
    password = data.get("password", "")
    dhcp = bool(data.get("dhcp", False))

    if not new_ip or not password:
        return web.json_response({"success": False, "error": "IP e Senha são obrigatórios"}, status=400)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None, engine.modify_device_ip, device_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp, brand
    )
    return web.json_response(result)

async def handle_activate_device(request):
    """Ativa uma câmera nova."""
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"success": False, "error": "JSON inválido"}, status=400)

    device_sn = data.get("serial", "")
    mac = data.get("mac", "")
    password = data.get("password", "")

    if not password:
        return web.json_response({"success": False, "error": "Senha é obrigatória para ativação"}, status=400)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, engine.activate_device, device_sn, mac, password)
    return web.json_response(result)

async def handle_batch_ip(request):
    """
    Altera IPs em sequência para múltiplas câmeras selecionadas.
    Ex: 192.168.1.100 -> .101, .102, .103...
    """
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"success": False, "error": "JSON inválido"}, status=400)

    devices = data.get("devices", [])
    start_ip = data.get("start_ip", "")
    mask = data.get("mask", "255.255.255.0")
    gateway = data.get("gateway", "")
    password = data.get("password", "")

    if not devices or not start_ip or not password:
        return web.json_response({"success": False, "error": "Dispositivos, IP inicial e Senha são obrigatórios"}, status=400)

    try:
        ip_parts = [int(p) for p in start_ip.split(".")]
    except Exception:
        return web.json_response({"success": False, "error": "Formato de IP inválido"}, status=400)

    results = []
    loop = asyncio.get_event_loop()

    for idx, dev in enumerate(devices):
        current_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{ip_parts[3] + idx}"
        res = await loop.run_in_executor(
            None, engine.modify_device_ip,
            dev.get("serial", ""), dev.get("mac", ""),
            current_ip, mask, gateway, dev.get("port", 80), password, False, dev.get("brand", "")
        )
        results.append({
            "mac": dev.get("mac"),
            "target_ip": current_ip,
            "status": res
        })

    return web.json_response({"success": True, "results": results})

async def handle_ping_test(request):
    """Testa conectividade rápida para o IP fornecido de forma 100% silenciosa."""
    ip = request.query.get("ip")
    if not ip:
        return web.json_response({"reachable": False, "error": "IP não informado"}, status=400)

    def do_ping():
        # Teste 1: Socket rápido nas portas de CFTV (instantâneo, sem processo externo)
        import socket
        for port in (80, 554, 8000, 37777):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.25)
                    if s.connect_ex((ip, port)) == 0:
                        return True
            except Exception:
                pass

        # Teste 2: Ping ICMP clássico oculto em segundo plano (sem console)
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            r = subprocess.run(
                ["ping", "-n", "1", "-w", "600", ip],
                capture_output=True,
                text=True,
                startupinfo=startupinfo,
                creationflags=flags
            )
            return r.returncode == 0
        except Exception:
            return False

    loop = asyncio.get_event_loop()
    reachable = await loop.run_in_executor(None, do_ping)
    return web.json_response({"ip": ip, "reachable": reachable})

async def on_startup(app):
    """Abre automaticamente a janela de aplicativo quando solicitado (100% camuflado)."""
    async def launch_ui():
        await asyncio.sleep(0.8)
        url = "http://localhost:37021"
        edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            if os.path.exists(edge):
                subprocess.Popen([edge, f"--app={url}"], startupinfo=startupinfo, creationflags=flags)
            elif os.path.exists(chrome):
                subprocess.Popen([chrome, f"--app={url}"], startupinfo=startupinfo, creationflags=flags)
            else:
                import webbrowser
                webbrowser.open(url)
        except Exception as e:
            print(f"[UI] Erro ao abrir janela: {e}")

    if "--open" in sys.argv:
        asyncio.create_task(launch_ui())

def make_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/interfaces", handle_get_interfaces)
    app.router.add_post("/api/scan", handle_scan)
    app.router.add_get("/api/devices", handle_get_devices)
    app.router.add_post("/api/demo", handle_demo_devices)
    app.router.add_post("/api/clear", handle_clear_devices)
    app.router.add_post("/api/devices/modify", handle_modify_device)
    app.router.add_post("/api/devices/activate", handle_activate_device)
    app.router.add_post("/api/devices/batch-ip", handle_batch_ip)
    app.router.add_get("/api/ping", handle_ping_test)
    app.router.add_static("/static/", PUBLIC_DIR)
    return app

if __name__ == "__main__":
    PORT = 37021
    print(f"=== NETSCAN CCTV — Servidor Iniciado na Porta {PORT} ===")
    print(f"-> Acesso Local: http://localhost:{PORT}")
    app = make_app()
    web.run_app(app, host="0.0.0.0", port=PORT)
