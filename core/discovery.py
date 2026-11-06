"""
Motor Central de Descoberta e Gerenciamento Multi-Protocolo (SADP, EZTools, ONVIF, Dahua).
Executa varredura concorrente em múltiplos sockets UDP e unifica resultados.
"""

import socket
import select
import time
import struct
import threading
from concurrent.futures import ThreadPoolExecutor

from .network import get_interfaces
from .hikvision import (
    build_sadp_probe, parse_sadp_response, build_sadp_modify_xml, build_sadp_activate_xml,
    HIKVISION_MULTICAST_GROUP, HIKVISION_SADP_PORT
)
from .onvif import build_onvif_probe, parse_onvif_response, ONVIF_MULTICAST_GROUP, ONVIF_PORT
from .uniview import build_unv_probe, parse_unv_response, build_unv_modify_packet, modify_uniview_lapi, UNV_MULTICAST_GROUP
from .dahua import build_dahua_probe, parse_dahua_response, build_dahua_modify_packet, DAHUA_DISCOVERY_PORT

class DiscoveryEngine:
    def __init__(self):
        self.devices = {}
        self.is_scanning = False
        self._lock = threading.Lock()

    def scan(self, target_interface_ip=None, timeout_sec=2.5):
        """
        Inicia uma varredura completa. Se target_interface_ip for fornecido,
        usa apenas essa placa. Caso contrário, dispara em todas as interfaces IPv4 ativas.
        """
        with self._lock:
            self.is_scanning = True
            self.devices = {}

        interfaces = get_interfaces()
        if target_interface_ip:
            interfaces = [i for i in interfaces if i["ip"] == target_interface_ip]
            if not interfaces:
                interfaces = [{"ip": target_interface_ip, "broadcast": "255.255.255.255", "name": "Manual"}]

        print(f"[Discovery] Iniciando varredura em {len(interfaces)} interface(s)...")

        # Probes a serem disparados
        sadp_pkt = build_sadp_probe()
        onvif_pkt = build_onvif_probe()
        unv_pkt = build_unv_probe()
        dahua_pkt = build_dahua_probe()

        sockets = []
        try:
            for iface in interfaces:
                local_ip = iface["ip"]
                bcast_ip = iface.get("broadcast", "255.255.255.255")

                # Socket 1: SADP / Uniview (Porta 37020)
                try:
                    s_sadp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    s_sadp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s_sadp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    try:
                        s_sadp.bind((local_ip, 0))
                    except Exception:
                        s_sadp.bind(("0.0.0.0", 0))
                    
                    # Definir interface de multicast de saída
                    try:
                        s_sadp.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))
                    except Exception:
                        pass

                    # Entrar no grupo multicast SADP
                    try:
                        mreq = struct.pack("4s4s", socket.inet_aton(HIKVISION_MULTICAST_GROUP), socket.inet_aton(local_ip))
                        s_sadp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
                    except Exception:
                        pass

                    # Disparar SADP e UNV
                    s_sadp.sendto(sadp_pkt, (HIKVISION_MULTICAST_GROUP, HIKVISION_SADP_PORT))
                    s_sadp.sendto(sadp_pkt, (bcast_ip, HIKVISION_SADP_PORT))
                    s_sadp.sendto(sadp_pkt, ("255.255.255.255", HIKVISION_SADP_PORT))
                    
                    s_sadp.sendto(unv_pkt, (UNV_MULTICAST_GROUP, HIKVISION_SADP_PORT))
                    s_sadp.sendto(unv_pkt, (bcast_ip, HIKVISION_SADP_PORT))

                    sockets.append((s_sadp, "sadp"))
                except Exception as e:
                    print(f"[Discovery] Erro ao criar socket SADP em {local_ip}: {e}")

                # Socket 2: ONVIF WS-Discovery (Porta 3702)
                try:
                    s_onvif = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    s_onvif.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s_onvif.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    try:
                        s_onvif.bind((local_ip, 0))
                    except Exception:
                        s_onvif.bind(("0.0.0.0", 0))

                    try:
                        s_onvif.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip))
                    except Exception:
                        pass

                    try:
                        mreq_onvif = struct.pack("4s4s", socket.inet_aton(ONVIF_MULTICAST_GROUP), socket.inet_aton(local_ip))
                        s_onvif.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq_onvif)
                    except Exception:
                        pass

                    s_onvif.sendto(onvif_pkt, (ONVIF_MULTICAST_GROUP, ONVIF_PORT))
                    s_onvif.sendto(onvif_pkt, (bcast_ip, ONVIF_PORT))

                    sockets.append((s_onvif, "onvif"))
                except Exception as e:
                    print(f"[Discovery] Erro ao criar socket ONVIF em {local_ip}: {e}")

                # Socket 3: Dahua / Intelbras (Porta 37810)
                try:
                    s_dh = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    s_dh.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    try:
                        s_dh.bind((local_ip, 0))
                    except Exception:
                        s_dh.bind(("0.0.0.0", 0))

                    s_dh.sendto(dahua_pkt, (bcast_ip, DAHUA_DISCOVERY_PORT))
                    s_dh.sendto(dahua_pkt, ("255.255.255.255", DAHUA_DISCOVERY_PORT))

                    sockets.append((s_dh, "dahua"))
                except Exception as e:
                    print(f"[Discovery] Erro ao criar socket Dahua em {local_ip}: {e}")

            # Loop de coleta com select
            start_time = time.time()
            all_socks = [s[0] for s in sockets]

            while (time.time() - start_time) < timeout_sec:
                readable, _, _ = select.select(all_socks, [], [], 0.2)
                for sock in readable:
                    try:
                        data, addr = sock.recvfrom(65535)
                        sender_ip = addr[0]
                        self._process_packet(data, sender_ip)
                    except Exception:
                        pass

        finally:
            for sock, _ in sockets:
                try:
                    sock.close()
                except Exception:
                    pass
            with self._lock:
                self.is_scanning = False

        print(f"[Discovery] Varredura finalizada. {len(self.devices)} dispositivo(s) encontrado(s).")
        return list(self.devices.values())

    def _process_packet(self, raw_data, sender_ip):
        """Processa o pacote bruto por todos os parsers e armazena sem duplicidade."""
        dev = None
        # Tenta SADP Hikvision
        if b"<Probe" in raw_data:
            dev = parse_sadp_response(raw_data, sender_ip)
        
        # Tenta ONVIF
        if not dev and (b"ProbeMatches" in raw_data or b"XAddrs" in raw_data):
            dev = parse_onvif_response(raw_data, sender_ip)

        # Tenta Uniview
        if not dev and (b"uniview" in raw_data.lower() or b"unv" in raw_data.lower()):
            dev = parse_unv_response(raw_data, sender_ip)

        # Tenta Dahua / Intelbras
        if not dev and (b"client.search" in raw_data or b"deviceType" in raw_data):
            dev = parse_dahua_response(raw_data, sender_ip)

        if dev and dev.get("ip"):
            dev_key = dev.get("mac") if dev.get("mac") and dev.get("mac") != "-" else dev["ip"]
            with self._lock:
                # Se já existe, atualiza mesclando informações mais ricas
                if dev_key in self.devices:
                    existing = self.devices[dev_key]
                    if existing["brand"] == "ONVIF Genérico" and dev["brand"] != "ONVIF Genérico":
                        existing["brand"] = dev["brand"]
                        existing["protocol"] = dev["protocol"]
                    if existing["model"] == "Câmera IP / NVR" and dev["model"] != "Câmera IP / NVR":
                        existing["model"] = dev["model"]
                    if dev.get("serial") and dev.get("serial") != "-":
                        existing["serial"] = dev["serial"]
                else:
                    self.devices[dev_key] = dev

    def modify_device_ip(self, device_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp=False, brand=None):
        """
        Envia comandos de alteração de IP adaptados por protocolo (Hikvision SADP, Uniview EZTools e Intelbras/Dahua).
        Se a marca não for explícita, dispara simultaneamente em todos os protocolos.
        """
        try:
            # 1. Localizar dispositivo em memória para identificar fabricante e IP atual
            target_dev = None
            with self._lock:
                for k, d in self.devices.items():
                    if (mac and d.get("mac", "").upper() == mac.upper()) or (device_sn and d.get("serial") == device_sn):
                        target_dev = d
                        break

            detected_brand = (brand or (target_dev.get("brand") if target_dev else "")).lower()
            current_ip = target_dev.get("ip") if target_dev else None
            current_port = target_dev.get("port", 80) if target_dev else 80

            is_hik = "hikvision" in detected_brand
            is_unv = "uniview" in detected_brand or "unv" in detected_brand
            is_dahua = "intelbras" in detected_brand or "dahua" in detected_brand
            is_all = not (is_hik or is_unv or is_dahua)

            # --- FLUXO 1: HIKVISION (SADP Protocol) ---
            if is_hik or is_all:
                try:
                    xml_data = build_sadp_modify_xml(device_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp)
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(xml_data, ("255.255.255.255", HIKVISION_SADP_PORT))
                    s.sendto(xml_data, (HIKVISION_MULTICAST_GROUP, HIKVISION_SADP_PORT))
                    s.close()
                except Exception as e:
                    print(f"[Hikvision Modify] Erro: {e}")

            # --- FLUXO 2: UNIVIEW (EZTools Protocol & LAPI) ---
            if is_unv or is_all:
                try:
                    # Pacote Broadcast UDP EZTools
                    unv_pkt = build_unv_modify_packet(device_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp)
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(unv_pkt, ("255.255.255.255", HIKVISION_SADP_PORT))
                    s.sendto(unv_pkt, ("255.255.255.255", 12345))
                    s.sendto(unv_pkt, (UNV_MULTICAST_GROUP, HIKVISION_SADP_PORT))
                    s.close()

                    # Fallback HTTP LAPI se o IP atual for acessível
                    if current_ip:
                        modify_uniview_lapi(current_ip, current_port, new_ip, new_mask, new_gateway, password)
                except Exception as e:
                    print(f"[Uniview Modify] Erro: {e}")

            # --- FLUXO 3: INTELBRAS / DAHUA (DHDiscover Protocol) ---
            if is_dahua or is_all:
                try:
                    dh_pkt = build_dahua_modify_packet(device_sn, mac, new_ip, new_mask, new_gateway, new_port, password, dhcp)
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                    s.sendto(dh_pkt, ("255.255.255.255", DAHUA_DISCOVERY_PORT))
                    s.close()
                except Exception as e:
                    print(f"[Dahua Modify] Erro: {e}")

            # Atualizar dados do dispositivo em memória local imediatamente
            if target_dev:
                with self._lock:
                    target_dev["ip"] = new_ip
                    target_dev["mask"] = new_mask
                    target_dev["gateway"] = new_gateway
                    target_dev["port"] = new_port
                    target_dev["dhcp"] = dhcp

            return {"success": True, "message": f"Comando de alteração de rede enviado com sucesso para {new_ip}."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def activate_device(self, device_sn, mac, password):
        """
        Envia comando de ativação para câmera inativa (Hikvision SADP e Uniview EZTools).
        """
        try:
            # 1. Hikvision SADP
            xml_data = build_sadp_activate_xml(device_sn, mac, password)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(xml_data, ("255.255.255.255", HIKVISION_SADP_PORT))
            s.sendto(xml_data, (HIKVISION_MULTICAST_GROUP, HIKVISION_SADP_PORT))
            s.close()

            # 2. Atualizar estado do dispositivo local
            with self._lock:
                for k, d in self.devices.items():
                    if (mac and d.get("mac", "").upper() == mac.upper()) or (device_sn and d.get("serial") == device_sn):
                        d["activated"] = True
                        break

            return {"success": True, "message": "Comando de ativação enviado com sucesso."}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Instância singleton global
engine = DiscoveryEngine()
