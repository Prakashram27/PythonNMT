#importing neccessory modules
import subprocess
import time

#getting own network hosts
def get_network_hosts():
    command = "nmap -sn --open --unprivileged 192.168.0.0/23 | grep 'Nmap scan report' | awk '{print $NF}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

   
    output = output.decode("utf-8")   # Decode the output from bytes to string
    lines = output.splitlines() # Split the output into lines

    #REturn
    return lines
start_time = time.time()
if __name__ == "__main__":
    # Get the network hosts
    network_hosts = get_network_hosts()

    command = "sudo tshark -a duration:30 -i wlp2s0 -T fields -e ip.src -e ip.dst -e ip.len"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output from bytes to string
    output = output.decode("utf-8")

    # Split the output into lines
    lines = output.splitlines()

    # Dictionary to store network host inbound usage,network host outbound usage,remote host inbound usage,remote host outbound usage
    network_host_inbound  = {}
    network_host_outbound = {}
    remote_host_inbound   = {}
    remote_host_outbound  = {}

    # Iterate through each line and extract the source IP, destination IP, and usage
    for line in lines:
        if line:
            values = line.split()
            if len(values) >= 3:
                source_ip, destination_ip, usage = values[:3]

                # Check if the source IP is a network host
                if source_ip in network_hosts:
                    if source_ip in network_host_outbound:
                        network_host_outbound[source_ip] += int(usage)
                    else:
                        network_host_outbound[source_ip] = int(usage)

                # # Check if the destination IP is a network host
                # if destination_ip in network_hosts:
                #     if destination_ip in network_host_inbound:
                #         network_host_inbound[destination_ip] += int(usage)
                #     else:
                #         network_host_inbound[destination_ip] = int(usage)

                # # Check if the source IP is a remote host
                # if source_ip not in network_hosts:
                #     if source_ip in remote_host_outbound:
                #         remote_host_outbound[source_ip] += int(usage)
                #     else:
                #         remote_host_outbound[source_ip] = int(usage)

                # Check if the destination IP is a remote host
                if destination_ip not in network_hosts:
                    if destination_ip in remote_host_inbound:
                        remote_host_inbound[destination_ip] += int(usage)
                    else:
                        remote_host_inbound[destination_ip] = int(usage)

    # # Determine the top inbound network host users
    # top_inbound_network_hosts = sorted(network_host_inbound.items(), key=lambda x: x[1], reverse=True)
    # print(top_inbound_network_hosts)

    # Determine the top outbound network host users
    top_outbound_network_hosts = sorted(network_host_outbound.items(), key=lambda x: x[1], reverse=True)
    print(top_outbound_network_hosts)

    # Determine the top inbound remote host users
    top_inbound_remote_hosts = sorted(remote_host_inbound.items(), key=lambda x: x[1], reverse=True)
    print(top_inbound_remote_hosts)

    # # Determine the top outbound remote host users
    # top_outbound_remote_hosts = sorted(remote_host_outbound.items(), key=lambda x: x[1], reverse=True)
    # print(top_outbound_remote_hosts)

end_time = time.time()

print(end_time - start_time)
