import socket
import ipaddress

def get_network_hosts():
    network = ipaddress.ip_network('192.168.0.0/23')
    live_hosts = []

    for host in network.hosts():
        ip = str(host)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)  # Set a timeout for the connection attempt
            result = sock.connect_ex((ip, 80))  # Attempt to connect to a common port (e.g., port 80)
            if result == 0:
                live_hosts.append(ip)
            sock.close()
        except socket.error:
            pass

    return live_hosts

host_list = get_network_hosts()
print(host_list)
