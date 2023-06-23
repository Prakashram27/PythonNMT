from scapy.all import ARP, Ether, srp
import time

def get_network_hosts():
    arp = ARP(pdst="192.168.0.0/23")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    hosts = []

    for sent, received in result:
        hosts.append(received.psrc)
    return hosts

network_hosts = get_network_hosts()

