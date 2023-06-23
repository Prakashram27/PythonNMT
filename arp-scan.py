import subprocess
import time 
from pprint import pprint

def clear_arp_cache():
    command = "sudo ip -s -s neigh flush all"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

def run_arp_scan():
    clear_arp_cache()  # Clear ARP cache before scanning

    command = "sudo arp-scan -l"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output from bytes to string
    output = output.decode("utf-8")

    # Split the output into lines
    lines = output.splitlines()

    ip_addresses = []
    for line in lines:
        if line.strip().startswith("192.168."):  # Modify the condition based on your IP address range
            ip_address = line.split()[0]
            ip_addresses.append(ip_address)
    print(ip_addresses)
    print(len(ip_addresses))
    set_values = set(ip_addresses)
    print(set_values)
    print(len(set_values))
    return ip_addresses

start_time = time.time()  # start time 
if __name__ == "__main__":
    discovered_ips = run_arp_scan()
    
end_time = time.time()
resulting_time = end_time - start_time
print(resulting_time) 