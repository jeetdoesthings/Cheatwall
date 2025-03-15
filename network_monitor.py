import psutil
import socket
from config import WHITELISTED_DOMAINS
from input_buffer_manager import add_input_event
from datetime import datetime
import pydivert

def resolve_domain(ip):
    """Resolve an IP address to its domain name."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def monitor_network():
    """Monitor network activity and log/block non-whitelisted domains."""
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                remote_ip = conn.raddr.ip
                remote_port = conn.raddr.port
                domain = resolve_domain(remote_ip)

                if domain:
                    # Check if the domain is whitelisted
                    if not any(whitelisted_domain in domain for whitelisted_domain in WHITELISTED_DOMAINS):
                        # Log suspicious activity
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        event_data = [
                            timestamp,
                            "Suspicious Network Activity",
                            "",
                            "",
                            "",
                            remote_ip,
                            domain,
                            "Blocked Connection",
                            f"Accessed non-whitelisted domain: {domain}"
                        ]
                        add_input_event(event_data)
                        print(f"Blocked connection to non-whitelisted domain: {domain} ({remote_ip}:{remote_port})")
    except Exception as e:
        print(f"Error monitoring network: {e}")

def block_non_whitelisted_domains():
    """Intercept and block packets to non-whitelisted domains."""
    with pydivert.WinDivert("tcp.DstPort == 80 or tcp.DstPort == 443") as w:
        for packet in w:
            domain = resolve_domain(packet.dst_addr)
            if domain and not any(whitelisted_domain in domain for whitelisted_domain in WHITELISTED_DOMAINS):
                print(f"Blocked packet to non-whitelisted domain: {domain}")
                continue  # Drop the packet
            w.send(packet)  # Allow the packet if the domain is whitelisted