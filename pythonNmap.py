import socket
import subprocess
import nmap
import time
from pprint import pprint


start_time = time.time()

#getting own network hosts
def get_network_hosts():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.0.0/23', arguments='-sn')

    hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            hosts.append(host)
    
    print(hosts)
    
    return hosts





get_network_hosts()
end_time = time.time()
print(end_time - start_time)