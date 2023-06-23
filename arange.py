import subprocess
import time
import nmap
from pprint import pprint

start_time = time.time()

def get_interface():
    command = "ip addr show | grep 'state UP' -A2 | awk -F: '{print $2}' | sed 's/^[[:space:]]*//'"
    print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    interfaces = output.decode("utf-8").splitlines()
    print(interfaces)
    return interfaces

def analyze_network(interface):
    print(interface)
    # Get the network hosts
    ip_range = '192.168.0.0/23'  # Update with your desired IP range
    network_hosts = get_network_hosts(ip_range)
    print(network_hosts)
    
    command = f"sudo tshark -a duration:10 -i {interface} -T fields -e ip.src -e ip.dst -e ip.len"
    print("command ==>",command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(output)

    # Decode the output from bytes to string
    output = output.decode("utf-8")

    # Split the output into lines
    lines = output.splitlines()
    print(lines)


    

    # Dictionary to store network host outbound usage and remote host inbound usage
    network_host_outbound = {}
    remote_host_inbound = {}
    dicts_value = {}


    # Iterate through each line and extract the source IP, destination IP, and usage
    for line in lines:
        if line:
            values = line.split()
            if len(values) >= 3:
                source_ip, destination_ip, usage = values[:3]
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",values)
                
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
                        print(1)
                    else:
                        remote_host_inbound[destination_ip] = int(usage)
                        print
    print(dicts_value)

    return network_host_outbound, remote_host_inbound

# getting own network hosts
def get_network_hosts(ip_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')
    hosts = []
    for host in nm.all_hosts():
        if nm[host].state() == 'up':
            hosts.append(host)
    return hosts

if __name__ == "__main__":
    # Get active network interfaces
    interfaces = get_interface()

    if len(interfaces) > 0:
        # Perform network analysis for each interface
        for interface in interfaces:
            print(f"Analyzing interface: {interface}")
            network_host_outbound, remote_host_inbound = analyze_network(interface)
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
