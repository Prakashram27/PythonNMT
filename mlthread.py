import subprocess
import time
import threading
import json
from pprint import pprint

debug = 1
sudo_password = None

# Get active network interfaces
# def get_interfaces():
#     command = "ip addr show | grep 'state UP' -A2 | awk -F: '{print $2}' | sed 's/^[[:space:]]*//'"
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, error = process.communicate()
#     interfaces = output.decode("utf-8").splitlines()
#     return interfaces
def get_physical_interfaces(
    file_loc="/home/chiefnet/ChiefNet/ConfigurationFiles",
    debug=0
):
    try:
        with open(file_loc+"/SystemConfiguration.json", "r") as f:
            system_config = json.load(f)
            print(system_config)
        # Get list from json file
        wan_interfaces_list = system_config["system_information"]["wan_interfaces"]
        lan_interfaces_list = system_config["system_information"]["lan_interfaces"]

        wifi_interfaces = []
        lan_interfaces = []
        wan_interfaces = []

        for interface in lan_interfaces_list:
            if (interface.lower().startswith("wl")):
                wifi_interfaces.append(interface)
            else:
                lan_interfaces.append(interface)

        wan_interfaces = [interface for interface in wan_interfaces_list
                          if not (interface.startswith("tun"))
                          ]

        return wan_interfaces, lan_interfaces, wifi_interfaces
    except Exception as e:
        if debug:
            raise e
        else:
            pass

def get_active_interfaces(interfaces, debug=0):
    """
    Function to retrieve active interfaces that are currently in UP state.
    """
    str_out = ""
    out = {}
    # Variable to store active interfaces.
    actives_interfaces = set()
    # cmd to get all the interfaces.
    command = f'ip -j address'

    # Executing the cmd
    cmd1 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    # Parsing the json to get desired "interfaces" only if its "operstate" is "UP".
    try:
        # Decoding cmd output
        str_out = cmd1.stdout.read().decode()

        # Decoding to dict format
        out = json.loads(str_out)

        # Looping through all the interfaces.
        for i in out:
            # Checking if the interface is in desired set of interfaces.
            if ((i.get("ifname")) != None):
                if (i["ifname"] in interfaces):
                    # Add to active interfaces set if state is UP.
                    if (i["operstate"].lower() == "up"):
                        actives_interfaces.add(i["ifname"])
                    # Add to active interfaces set if state is UNKNOWN.
                    elif (i["operstate"].lower() == "unknown"):
                        actives_interfaces.add(i["ifname"])
                    # Add to logs if state is neither UP nor DOWN.
                    elif (i["operstate"].lower() != 'down'):
                        pass

    except Exception as e:
        if debug:
            raise e
        else:
            pass
#    print(actives_interfaces)
    return actives_interfaces, str(str_out)



# Perform network analysis for a specific interface
def analyze_interface(interface):
    start = time.time()

    # Get the network hosts
    ip_range = '192.168.0.0/23'  # Update with your desired IP range
    network_hosts = run_arp_scan()

    command = f"sudo tshark -a duration:30 -i {interface} -T fields -e ip.src -e ip.dst -e ip.len"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output from bytes to string
    output = output.decode("utf-8")

    # Split the output into lines
    lines = output.splitlines()

    # Process the output and extract relevant information
    network_host_outbound = {}
    remote_host_inbound = {}

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

                # Check if the destination IP is a remote host
                if destination_ip not in network_hosts:
                    if destination_ip in remote_host_inbound:
                        remote_host_inbound[destination_ip] += int(usage)
                    else:
                        remote_host_inbound[destination_ip] = int(usage)

    # Process the results as needed
    print(f"Results for interface: {interface}")
    print("Top Outbound Network Hosts:")
    pprint(sorted(network_host_outbound.items(), key=lambda x: x[1], reverse=True))
    print("Top Inbound Remote Hosts:")
    pprint(sorted(remote_host_inbound.items(), key=lambda x: x[1], reverse=True))

    print(f"Execution time for interface {interface}: {time.time() - start}")

# Clear ARP cache
def clear_arp_cache():
    command = "sudo ip -s -s neigh flush all"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

# Run ARP scan
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

    try:
       # print(datetime.datetime.now())

        result = get_physical_interfaces(
            r"/etc/telegraf/custom_scripts",
            debug
        )
        if (result == None):
            raise Exception("No interfaces found.")
        wan_interfaces, lan_interfaces, wifi_interfaces = result

        #interfaces = set(list(wan_interface_dict) + list(lan_interface_dict))
        interfaces = set(wan_interfaces + lan_interfaces + wifi_interfaces)
        #interfaces = {"enp1s0","enp2s0","enp3s0","enp4s0"}
        inactives_interfaces = set()

        # Getting active interfaces.
        actives_interfaces, out = get_active_interfaces(interfaces=interfaces,
                                                        debug=debug
                                                        )
        # getting inactive interfaces
        inactives_interfaces = interfaces - actives_interfaces
        
#        print(actives_interfaces)
        # Printing line protocol for interfaces present.
        for interface in actives_interfaces:
            # Iftop data for active interfaces.
            analyze_interface(sudo_password=sudo_password,
                      interface=interface,
                      debug=debug
                      )
       # print(datetime.datetime.now())

    except Exception as e:
        if debug:
            raise e
        else:
            pass
