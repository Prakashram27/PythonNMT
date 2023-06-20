import subprocess

if __name__ == "__main__":
    command = "sudo tshark -a duration:30 -i wlp2s0 -T fields -e ip.src -e ip.dst -e ip.len" 
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output from bytes to string
    output = output.decode("utf-8")

    # Split the output into lines
    lines = output.splitlines()

    network_host_inbound = {}
    network_host_outbound = {}
    remote_host_inbound = {}
    remote_host_outbound = {}

    # Iterate through each line and extract the source IP, destination IP, and usage
    for line in lines:
        if line:
            values = line.split()
            if len(values) >= 3:
                source_ip, destination_ip, usage = values[:3]

                # Check if the source IP is a network host
                if source_ip.startswith("192.168"):
                    if source_ip in network_host_outbound:
                        network_host_outbound[source_ip] += int(usage)
                    else:
                        network_host_outbound[source_ip] = int(usage)

                # Check if the destination IP is a network host
                if destination_ip.startswith("192.168"):
                    if destination_ip in network_host_inbound:
                        network_host_inbound[destination_ip] += int(usage)
                    else:
                        network_host_inbound[destination_ip] = int(usage)

                # Check if the source IP is a remote host
                if not source_ip.startswith("192.168"):
                    if source_ip in remote_host_outbound:
                        remote_host_outbound[source_ip] += int(usage)
                    else:
                        remote_host_outbound[source_ip] = int(usage)

                # Check if the destination IP is a remote host
                if not destination_ip.startswith("192.168"):
                    if destination_ip in remote_host_inbound:
                        remote_host_inbound[destination_ip] += int(usage)
                    else:
                        remote_host_inbound[destination_ip] = int(usage)

    # Determine the top inbound network host users
    top_inbound_network_hosts = sorted(network_host_inbound.items(), key=lambda x: x[1], reverse=True)

    print("Top Inbound Network Host Users:")
    for host, usage in top_inbound_network_hosts:
        print("Host:", host)
        print("Usage:", usage)

    # Determine the top outbound network host users
    top_outbound_network_hosts = sorted(network_host_outbound.items(), key=lambda x: x[1], reverse=True)

    print("Top Outbound Network Host Users:")
    for host, usage in top_outbound_network_hosts:
        print("Host:", host)
        print("Usage:", usage)


    # Determine the top inbound remote host users
    top_inbound_remote_hosts = sorted(remote_host_inbound.items(), key=lambda x: x[1], reverse=True)

    print("Top Inbound Remote Host Users:")
    for host, usage in top_inbound_remote_hosts:
        print("Host:", host)
        print("Usage:", usage)
        

    # Determine the top outbound remote host users
    top_outbound_remote_hosts = sorted(remote_host_outbound.items(), key=lambda x: x[1], reverse=True)

    print("Top Outbound Remote Host Users:")
    for host, usage in top_outbound_remote_hosts:
        print("Host:", host)
        print("Usage:", usage)
