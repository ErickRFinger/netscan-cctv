"""
Módulo Uniview (EZTools Protocol & LAPI).
Implementa descoberta proprietária UNV em UDP, integração com LAPI HTTP e WS-Discovery.
Permite descoberta e alteração de parâmetros de rede para câmeras e NVRs Uniview.
"""

import json
import re
import socket
import urllib.request
import base64

UNV_DISCOVERY_PORTS = [37020, 12345, 3702]
UNV_MULTICAST_GROUP = "239.255.255.250"

def build_unv_probe():
    """
    Gera o pacote de busca Uniview EZTools (Broadcast / Multicast).
    Suporta formato JSON e binário de probe.
    """
    probe_dict = {
        "Method": "Probe",
        "Params": {
            "Types": ["NetworkVideoTransmitter"],
            "Target": "All"
        }
    }
    return json.dumps(probe_dict).encode("utf-8")

def parse_unv_response(raw_bytes, sender_ip=None):
    """
    Decodifica respostas do protocolo EZTools / Uniview LAPI.
    """
    try:
        text = raw_bytes.decode("utf-8", errors="ignore").strip()
        # Verificar se é resposta JSON da Uniview
        if text.startswith("{") and ("uniview" in text.lower() or "unv" in text.lower()):
            data = json.loads(text)
            params = data.get("Params", data.get("Response", {}))
            
            mac = params.get("MAC", "").upper()
            ip = params.get("IPv4Address", params.get("IP", sender_ip))
            mask = params.get("IPv4SubnetMask", params.get("SubnetMask", "255.255.255.0"))
            gw = params.get("IPv4Gateway", params.get("Gateway", ""))
            port = params.get("Port", params.get("HttpPort", 80))
            model = params.get("Model", params.get("DeviceType", "Câmera Uniview"))
            sn = params.get("Serial", params.get("DeviceSN", "-"))
            fw = params.get("Firmware", params.get("SoftwareVersion", "-"))
            activated = params.get("Activated", True)

            return {
                "id": mac or f"unv_{ip}",
                "brand": "Uniview",
                "model": model,
                "serial": sn,
                "mac": mac or "-",
                "ip": ip,
                "mask": mask,
                "gateway": gw,
                "port": int(port) if str(port).isdigit() else 80,
                "version": fw,
                "activated": bool(activated),
                "dhcp": bool(params.get("DHCP", False)),
                "protocol": "EZTools (Uniview)",
                "vendor_icon": "uniview"
            }
    except Exception:
        pass
    return None

def build_unv_modify_packet(dev_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp=False):
    """
    Monta pacote de alteração de IP no padrão EZTools da Uniview.
    """
    clean_mac = mac.replace("-", ":").upper()
    payload = {
        "Method": "ModifyNetworkParam",
        "Params": {
            "MAC": clean_mac,
            "DeviceSN": dev_sn,
            "IPv4Address": new_ip,
            "IPv4SubnetMask": new_mask,
            "IPv4Gateway": new_gateway,
            "Port": new_port,
            "Password": password,
            "DHCP": dhcp
        }
    }
    return json.dumps(payload).encode("utf-8")

def modify_uniview_lapi(current_ip, port, new_ip, new_mask, new_gateway, password):
    """
    Altera IP de câmera Uniview via LAPI HTTP REST (quando o IP atual for roteável).
    """
    try:
        url = f"http://{current_ip}:{port}/LAPI/V1.0/System/Network/Interfaces/1/IPv4"
        body = json.dumps({
            "IPv4Address": new_ip,
            "IPv4SubnetMask": new_mask,
            "IPv4Gateway": new_gateway
        }).encode("utf-8")
        
        req = urllib.request.Request(url, data=body, method="PUT")
        req.add_header("Content-Type", "application/json")
        auth_str = base64.b64encode(f"admin:{password}".encode("utf-8")).decode("ascii")
        req.add_header("Authorization", f"Basic {auth_str}")
        
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            return resp.status in (200, 204)
    except Exception:
        return False
