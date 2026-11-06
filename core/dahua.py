"""
Módulo Intelbras & Dahua (DHDiscover Protocol).
Implementa descoberta de DVRs, NVRs e Câmeras IP Intelbras/Dahua via UDP 37810.
Suporta alteração de parâmetros de rede via pacote client.modifyIP.
"""

import json
import re

DAHUA_DISCOVERY_PORT = 37810

def build_dahua_probe():
    """Gera o pacote de busca DHDiscover (JSON e Header)."""
    payload = {
        "method": "client.search",
        "params": {
            "mac": ""
        }
    }
    return json.dumps(payload).encode("utf-8")

def parse_dahua_response(raw_bytes, sender_ip=None):
    """
    Decodifica resposta do protocolo DHDiscover da Intelbras/Dahua.
    """
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
        # Procura por estrutura JSON na resposta
        idx = text.find("{")
        if idx != -1:
            json_str = text[idx:]
            end_idx = json_str.rfind("}")
            if end_idx != -1:
                json_str = json_str[:end_idx+1]
                data = json.loads(json_str)
                params = data.get("params", data.get("result", {}))
                
                mac = params.get("mac", "").upper()
                ip = params.get("ip", sender_ip)
                mask = params.get("netmask", "255.255.255.0")
                gw = params.get("gateway", "")
                port = params.get("port", 80)
                model = params.get("deviceType", params.get("model", "Dispositivo Intelbras/Dahua"))
                sn = params.get("serialNo", "-")
                version = params.get("version", "-")

                # Identifica se é marca Intelbras ou Dahua
                brand = "Intelbras" if "intelbras" in model.lower() or "vip" in model.lower() or "vhd" in model.lower() else "Intelbras / Dahua"

                return {
                    "id": mac or f"dh_{ip}",
                    "brand": brand,
                    "model": model,
                    "serial": sn,
                    "mac": mac or "-",
                    "ip": ip,
                    "mask": mask,
                    "gateway": gw,
                    "port": int(port) if str(port).isdigit() else 80,
                    "version": version,
                    "activated": True,
                    "dhcp": bool(params.get("dhcp", False)),
                    "protocol": "DHDiscover (Intelbras/Dahua)",
                    "vendor_icon": "intelbras"
                }
    except Exception:
        pass
    return None

def build_dahua_modify_packet(dev_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp=False):
    """
    Monta pacote de alteração de IP no padrão DHDiscover da Intelbras/Dahua.
    """
    clean_mac = mac.replace("-", ":").upper()
    payload = {
        "method": "client.modifyIP",
        "params": {
            "mac": clean_mac,
            "ip": new_ip,
            "netmask": new_mask,
            "gateway": new_gateway,
            "password": password,
            "dhcp": dhcp
        }
    }
    return json.dumps(payload).encode("utf-8")
