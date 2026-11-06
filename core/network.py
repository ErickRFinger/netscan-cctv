"""
Módulo de detecção e gerenciamento de interfaces de rede para Windows.
Descobre placas físicas (Ethernet/Wi-Fi), calcula sub-redes e broadcasts.
Totalmente oculto e sem janelas de console (CREATE_NO_WINDOW).
"""

import sys
import socket
import subprocess
import re
import json
import time

_interfaces_cache = []
_cache_time = 0
CACHE_TTL = 12.0  # Cache de 12 segundos para evitar chamadas repetidas ao SO

def get_interfaces(force=False):
    """
    Lista todas as interfaces de rede ativas com IPv4 válido usando PowerShell.
    Executa de forma 100% oculta em segundo plano (sem piscar janela preta).
    """
    global _interfaces_cache, _cache_time
    now = time.time()
    
    if not force and _interfaces_cache and (now - _cache_time < CACHE_TTL):
        return _interfaces_cache

    interfaces = []
    try:
        cmd = [
            "powershell", "-NoProfile", "-NonInteractive", "-WindowStyle", "Hidden", "-Command",
            """
            Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } | ForEach-Object {
                $iface = Get-NetAdapter -InterfaceIndex $_.InterfaceIndex -ErrorAction SilentlyContinue
                [PSCustomObject]@{
                    Index = $_.InterfaceIndex
                    Alias = $_.InterfaceAlias
                    IP = $_.IPAddress
                    PrefixLength = $_.PrefixLength
                    Status = $iface.Status
                    LinkSpeed = $iface.LinkSpeed
                }
            } | ConvertTo-Json -Compress
            """
        ]
        
        # Garante ocultação total no Windows (sem console pop-up)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE

        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            startupinfo=startupinfo,
            creationflags=creationflags
        )
        out = res.stdout.strip()
        if out:
            data = json.loads(out)
            if isinstance(data, dict):
                data = [data]
            for item in data:
                ip = item.get("IP")
                prefix = item.get("PrefixLength", 24)
                mask = prefix_to_mask(prefix)
                bcast = calculate_broadcast(ip, mask)
                interfaces.append({
                    "index": item.get("Index"),
                    "name": item.get("Alias"),
                    "ip": ip,
                    "mask": mask,
                    "prefix": prefix,
                    "broadcast": bcast,
                    "status": item.get("Status", "Up"),
                    "speed": item.get("LinkSpeed", "Desconhecido")
                })
        if interfaces:
            _interfaces_cache = interfaces
            _cache_time = now
    except Exception as e:
        # Fallback padrão seguro usando socket nativo sem subprocess
        try:
            hostname = socket.gethostname()
            for ip in socket.gethostbyname_ex(hostname)[2]:
                if not ip.startswith("127.") and not ip.startswith("169.254."):
                    interfaces.append({
                        "index": 0,
                        "name": f"Interface ({ip})",
                        "ip": ip,
                        "mask": "255.255.255.0",
                        "prefix": 24,
                        "broadcast": "255.255.255.255",
                        "status": "Up",
                        "speed": "-"
                    })
            if interfaces:
                _interfaces_cache = interfaces
                _cache_time = now
        except Exception:
            pass

    return interfaces

def prefix_to_mask(prefix):
    """Converte tamanho de prefixo (ex: 24) para máscara IPv4 (255.255.255.0)."""
    mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return f"{(mask_int >> 24) & 0xFF}.{(mask_int >> 16) & 0xFF}.{(mask_int >> 8) & 0xFF}.{mask_int & 0xFF}"

def calculate_broadcast(ip_str, mask_str):
    """Calcula o endereço IPv4 de broadcast a partir do IP e da máscara."""
    try:
        ip_parts = [int(p) for p in ip_str.split(".")]
        mask_parts = [int(p) for p in mask_str.split(".")]
        bcast_parts = [(ip_parts[i] | (~mask_parts[i] & 0xFF)) for i in range(4)]
        return ".".join(str(p) for p in bcast_parts)
    except Exception:
        return "255.255.255.255"

if __name__ == "__main__":
    ifaces = get_interfaces(force=True)
    print("Interfaces detectadas:")
    for iface in ifaces:
        print(f" - [{iface['name']}] IP: {iface['ip']} / Mask: {iface['mask']} -> Bcast: {iface['broadcast']}")
