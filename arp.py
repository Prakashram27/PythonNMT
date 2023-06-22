from scapy.all import ARP, Ether, srp
import time

start_time = time.time()
def get_network_hosts():
    print('starts')
    # Create an ARP request packet
    arp = ARP(pdst="192.168.0.0/23")
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and capture the responses
    result = srp(packet, timeout=3, verbose=0)[0]

    # Extract the IP addresses of the responding hosts
    hosts = []
    for sent, received in result:
        hosts.append(received.psrc)

    return hosts
network_hosts = get_network_hosts()
print(network_hosts)
end_time = time.time()
print(end_time-start_time)
