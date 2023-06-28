import subprocess
import time
import nmap
from pprint import pprint

start_time = time.time()

def get_interface():
    command = "ip addr show | grep 'state UP' -A2 | awk -F: '{print $2}' | sed 's/^[[:space:]]*//'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    interfaces = output.decode("utf-8").splitlines()
    # return interfaces
    return ['wlp2s0']

def analyze_network():
    start = time.time()

    # Get the network hosts
    interface = 'wlp2s0'
    ip_range = '192.168.0.0/23'  # Update with your desired IP range
    network_hosts = run_arp_scan()
    
    command = f"sudo tshark -a duration:30 -i {interface} -T fields -e ip.src -e ip.dst -e ip.len"
    print("command ==>",command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    # print(output)

    # Decode the output from bytes to string
    output = output.decode("utf-8")
    print(time.time() - start)
    # Split the output into lines
    lines = output.splitlines()

    # Dictionary to store network host outbound usage and remote host inbound usage
    network_host_outbound = {}
    remote_host_inbound = {}


    # Iterate through each line and extract the source IP, destination IP, and usage
    for line in lines:
        if line:
            values = line.split()
            if len(values) >= 3:
                source_ip, destination_ip, usage = values[:3]
                # print(values[:3]) #   NEED TO IMPROVE HERE 
            
            # Check if the source IP is a network host
                if source_ip in network_hosts:
                    if source_ip in network_host_outbound:
                        network_host_outbound[source_ip] += int(usage)
                    else:
                        network_host_outbound[source_ip] = int(usage)

            # Check if the destination IP is a remote host
                if destination_ip not in network_hosts:
                    if destination_ip in remote_host_inbound:
                        remote_host_inbound[destination_ip] += int(usage)
                    else:
                        remote_host_inbound[destination_ip] = int(usage)

    return network_host_outbound, remote_host_inbound

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
    return ip_addresses

if __name__ == "__main__":
    start_time = time.time()
    # Get active network interfaces
    interfaces = get_interface()

    if len(interfaces) > 0:
        # Perform network analysis for each interface
        for interface in interfaces:
            print(f"Analyzing interface: {interface}")
            network_host_outbound, remote_host_inbound = analyze_network()
            print(network_host_outbound)
            print(remote_host_inbound)
            # Determine the top outbound network host users
            top_outbound_network_hosts = sorted(network_host_outbound.items(), key=lambda x: x[1], reverse=True)
            print("Top Outbound Network Hosts:")
            pprint(top_outbound_network_hosts)
            # Determine the top inbound remote host users
            top_inbound_remote_hosts = sorted(remote_host_inbound.items(), key=lambda x: x[1], reverse=True)
            print("Top Inbound Remote Hosts:")
            pprint(top_inbound_remote_hosts)
    end_time = time.time()
    print(end_time-start_time)

