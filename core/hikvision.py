"""
Módulo de Protocolo Hikvision SADP (Search Active Devices Protocol).
Implementa descoberta L2/L3 UDP (37020), ativação e alteração de parâmetros de rede.
"""

import uuid
import xml.etree.ElementTree as ET
import re

HIKVISION_MULTICAST_GROUP = "239.255.255.250"
HIKVISION_SADP_PORT = 37020

def build_sadp_probe():
    """Gera o pacote XML de inquiry do SADP."""
    probe_uuid = str(uuid.uuid4()).upper()
    xml_str = (
        '<?xml version="1.0" encoding="utf-8"?>'
        f'<Probe><Uuid>{probe_uuid}</Uuid><Types>inquiry</Types></Probe>'
    )
    return xml_str.encode("utf-8")

def parse_sadp_response(raw_bytes, sender_ip=None):
    """
    Decodifica o pacote XML de resposta <ProbeMatch> da Hikvision.
    Retorna dicionário padronizado com os dados da câmera.
    """
    try:
        text = raw_bytes.decode("utf-8", errors="ignore").strip()
        if not ("<ProbeMatch" in text or "<Probe" in text):
            return None
        
        # Limpar cabeçalhos ou ruídos antes da tag XML
        start = text.find("<ProbeMatch")
        if start == -1:
            start = text.find("<?xml")
        if start != -1:
            text = text[start:]
        end = text.rfind(">")
        if end != -1:
            text = text[:end+1]

        def get_tag(tag, default=""):
            m = re.search(rf"<{tag}>(.*?)</{tag}>", text, re.IGNORECASE | re.DOTALL)
            return m.group(1).strip() if m else default

        dev_type = get_tag("DeviceType")
        dev_desc = get_tag("DeviceDescription") or get_tag("DeviceType")
        dev_sn = get_tag("DeviceSN")
        mac = get_tag("MAC").upper().replace("-", ":")
        ipv4 = get_tag("IPv4Address") or sender_ip
        mask = get_tag("IPv4SubnetMask", "255.255.255.0")
        gateway = get_tag("IPv4Gateway", "")
        http_port = get_tag("HttpPort", "80")
        sw_version = get_tag("SoftwareVersion") or get_tag("DSPVersion")
        activated_str = get_tag("Activated", "true").lower()
        dhcp_str = get_tag("DHCP", "false").lower()

        # Se não achou MAC via tag, tenta deduzir do SN se for padrão Hikvision
        if not mac and dev_sn:
            mac_match = re.search(r"([0-9A-Fa-f]{12})", dev_sn)
            if mac_match:
                raw_mac = mac_match.group(1)
                mac = ":".join(raw_mac[i:i+2] for i in range(0, 12, 2)).upper()

        return {
            "id": mac or f"hik_{ipv4}",
            "brand": "Hikvision",
            "model": dev_desc or dev_type or "Câmera / NVR Hikvision",
            "serial": dev_sn,
            "mac": mac or "-",
            "ip": ipv4,
            "mask": mask,
            "gateway": gateway,
            "port": int(http_port) if http_port.isdigit() else 80,
            "version": sw_version or "-",
            "activated": activated_str in ["true", "1", "yes"],
            "dhcp": dhcp_str in ["true", "1", "yes"],
            "protocol": "SADP (Hikvision)",
            "vendor_icon": "hikvision"
        }
    except Exception as e:
        print(f"[Hikvision] Erro no parsing: {e}")
        return None

def build_sadp_modify_xml(dev_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp=False):
    """
    Monta pacote XML para alterar parâmetros de rede da Hikvision.
    """
    clean_mac = mac.replace(":", "-").upper()
    xml_str = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<SetDeviceParam>'
        f'<DeviceSN>{dev_sn}</DeviceSN>'
        f'<MAC>{clean_mac}</MAC>'
        f'<IPv4Address>{new_ip}</IPv4Address>'
        f'<IPv4SubnetMask>{new_mask}</IPv4SubnetMask>'
        f'<IPv4Gateway>{new_gateway}</IPv4Gateway>'
        f'<HttpPort>{new_port}</HttpPort>'
        f'<Password>{password}</Password>'
        f'<DHCP>{"true" if dhcp else "false"}</DHCP>'
        '</SetDeviceParam>'
    )
    return xml_str.encode("utf-8")

def build_sadp_activate_xml(dev_sn, mac, password):
    """
    Monta pacote XML para ativação de câmera Hikvision recém-tirada da caixa.
    """
    clean_mac = mac.replace(":", "-").upper()
    xml_str = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<Activate>'
        f'<DeviceSN>{dev_sn}</DeviceSN>'
        f'<MAC>{clean_mac}</MAC>'
        f'<Password>{password}</Password>'
        '</Activate>'
    )
    return xml_str.encode("utf-8")
