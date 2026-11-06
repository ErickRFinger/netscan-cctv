"""
Módulo ONVIF WS-Discovery (Web Services Discovery).
Protocolo padrão da indústria suportado por Uniview, Hikvision, Intelbras, Axis, etc.
Porta UDP 3702, Multicast 239.255.255.250.
"""

import uuid
import re
from urllib.parse import urlparse

ONVIF_MULTICAST_GROUP = "239.255.255.250"
ONVIF_PORT = 3702

def build_onvif_probe():
    """Gera o envelope SOAP para busca WS-Discovery ONVIF."""
    msg_id = str(uuid.uuid4())
    soap_str = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<e:Envelope xmlns:e="http://www.w3.org/2003/05/soap-envelope" '
        'xmlns:w="http://schemas.xmlsoap.org/ws/2004/08/addressing" '
        'xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" '
        'xmlns:dn="http://www.onvif.org/ver10/network/wsdl">'
        '<e:Header>'
        f'<w:MessageID>uuid:{msg_id}</w:MessageID>'
        '<w:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</w:To>'
        '<w:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</w:Action>'
        '</e:Header>'
        '<e:Body>'
        '<d:Probe>'
        '<d:Types>dn:NetworkVideoTransmitter</d:Types>'
        '</d:Probe>'
        '</e:Body>'
        '</e:Envelope>'
    )
    return soap_str.encode("utf-8")

def parse_onvif_response(raw_bytes, sender_ip=None):
    """
    Decodifica o ProbeMatches SOAP e extrai modelo, fabricante e endereço do serviço.
    """
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
        if "ProbeMatches" not in text and "XAddrs" not in text:
            return None

        # Extrair XAddrs (URL do serviço ONVIF)
        m_xaddrs = re.search(r"<(?:[^:]+:)?XAddrs>(.*?)</(?:[^:]+:)?XAddrs>", text, re.IGNORECASE | re.DOTALL)
        xaddrs_raw = m_xaddrs.group(1).strip() if m_xaddrs else ""
        first_url = xaddrs_raw.split()[0] if xaddrs_raw else ""

        ip = sender_ip
        port = 80
        if first_url:
            parsed = urlparse(first_url)
            if parsed.hostname:
                ip = parsed.hostname
            if parsed.port:
                port = parsed.port

        # Extrair Scopes (onde vem fabricante, modelo, localização)
        m_scopes = re.search(r"<(?:[^:]+:)?Scopes>(.*?)</(?:[^:]+:)?Scopes>", text, re.IGNORECASE | re.DOTALL)
        scopes_raw = m_scopes.group(1).strip() if m_scopes else ""
        
        brand = "ONVIF Genérico"
        model = "Câmera IP / NVR"
        mac = "-"
        
        # Parse dos scopes da ONVIF (onvif://www.onvif.org/...)
        for s in scopes_raw.split():
            s_lower = s.lower()
            if "uniview" in s_lower or "unv" in s_lower:
                brand = "Uniview"
            elif "hikvision" in s_lower:
                brand = "Hikvision"
            elif "dahua" in s_lower or "intelbras" in s_lower:
                brand = "Intelbras / Dahua"
            
            # Hardware / Modelo
            if "/hardware/" in s:
                model = s.split("/hardware/")[-1]
            elif "/name/" in s and model == "Câmera IP / NVR":
                model = s.split("/name/")[-1]
            elif "/mac/" in s_lower:
                mac = s.split("/")[-1].upper()

        if not ip:
            return None

        return {
            "id": mac if mac != "-" else f"onvif_{ip}_{port}",
            "brand": brand,
            "model": model,
            "serial": "-",
            "mac": mac,
            "ip": ip,
            "mask": "255.255.255.0",
            "gateway": "",
            "port": port,
            "version": "ONVIF Profile S/T",
            "activated": True,
            "dhcp": False,
            "protocol": f"ONVIF ({brand})",
            "xaddrs": first_url,
            "vendor_icon": brand.lower().split()[0]
        }
    except Exception as e:
        print(f"[ONVIF] Erro no parsing: {e}")
        return None
