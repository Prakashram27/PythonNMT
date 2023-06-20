# import re
# from collections import defaultdict
# import subprocess

# # Regex patterns to extract relevant information
# packet_pattern = r'> (\w+) \d+ \d+s\.\d+ns #\d+'
# ip_pattern = r'IPv4 Addr \((.*?) => (.*?)\)'
# data_off_pattern = r'DataOff \((\d+)\)'
# length_pattern = r'Len \((\d+)\)'

# # Dictionary to store bandwidth usage for each IP
# bandwidth_usage = defaultdict(int)

# # Run netsniff-ng command and capture the output
# # command = "sudo netsniff-ng -i wlp2s0"
# # output = subprocess.check_output(command, shell=True, text=True)

# output = """< enp1s0 66 1686655580s.523649734ns #114
# [ Eth MAC (e4:b3:18:dd:8e:ac => 00:a0:c9:4c:60:92), Proto (0x0800, IPv4) ]
# [ Vendor (Unknown => INTEL CORPORATION - HF1-06) ]
# [ IPv4 Addr (192.168.0.151 => 192.168.0.104), Proto (6), TTL (64), TOS (16), Ver (4), IHL (5), Tlen (52), ID (41325), Res (0), NoFrag (1), MoreF rag (0), FragOff (0), CSum (0x16f7) is ok ]
# [ TCP Port (37290 => 5000 (upnp)), SN (0xe1020328), AN (0xaeb03cb1), DataOff (8), Res (0), Flags (ACK), Window (5719), CSum (0x2b2d), Ur gPtr (0) ]
# [ Chr .....Tpw..N. ]
# [ Hex 01 01 08 0a ad 54 70 77 d1 b5 4e a8 ]
# """

# # Extract information from each packet
# packets = re.findall(packet_pattern, output)
# for packet in packets:
#     source_ip, dest_ip = re.findall(ip_pattern, packet)[0]
#     data_offset = int(re.findall(data_off_pattern, packet)[0])
#     packet_length = int(re.findall(length_pattern, packet)[0])
#     bandwidth_usage[source_ip] += packet_length - data_offset

# # Get the top bandwidth user
# top_bandwidth_user = max(bandwidth_usage, key=bandwidth_usage.get)
# top_bandwidth = bandwidth_usage[top_bandwidth_user]

# # Get the top remote host
# remote_hosts = set()
# for packet in packets:
#     source_ip, dest_ip = re.findall(ip_pattern, packet)[0]
#     if source_ip == top_bandwidth_user:
#         remote_hosts.add(dest_ip)
# top_remote_host = ', '.join(remote_hosts)

# # Calculate the total bandwidth usage
# total_bandwidth = sum(bandwidth_usage.values())

# # Print the results
# print("Top Bandwidth User:", top_bandwidth_user)
# print("Top Remote Host:", top_remote_host)
# print("Total Bandwidth Usage:", total_bandwidth)


import re
from collections import defaultdict

# Regex patterns to extract relevant information
packet_pattern = r'> (\w+) \d+ \d+s\.\d+ns #\d+'
ip_pattern = r'IPv4 Addr \((.*?) => (.*?)\)'
data_off_pattern = r'DataOff \((\d+)\)'
length_pattern = r'Len \((\d+)\)'

# Dictionary to store bandwidth usage for each IP
bandwidth_usage = defaultdict(int)

output = "< enp1s0 66 1686655580s.523649734ns #114 [ Eth MAC (e4:b3:18:dd:8e:ac => 00:a0:c9:4c:60:92), Proto (0x0800, IPv4) ] [ Vendor (Unknown => INTEL CORPORATION - HF1-06) ] [ IPv4 Addr (192.168.0.151 => 192.168.0.104), Proto (6), TTL (64), TOS (16), Ver (4), IHL (5), Tlen (52), ID (41325), Res (0), NoFrag (1), MoreF rag (0), FragOff (0), CSum (0x16f7) is ok ] [ TCP Port (37290 => 5000 (upnp)), SN (0xe1020328), AN (0xaeb03cb1), DataOff (8), Res (0), Flags (ACK), Window (5719), CSum (0x2b2d), Ur gPtr (0) ] [ Chr .....Tpw..N. ] [ Hex 01 01 08 0a ad 54 70 77 d1 b5 4e a8 ]"

# Extract information from each packet
packets = re.findall(packet_pattern, output)
for packet in packets:
    source_ip, dest_ip = re.findall(ip_pattern, packet)[0]
    data_offset = int(re.findall(data_off_pattern, packet)[0])
    packet_length = int(re.findall(length_pattern, packet)[0])
    bandwidth_usage[source_ip] += packet_length - data_offset

# Get the top bandwidth user
top_bandwidth_user = max(bandwidth_usage, key=bandwidth_usage.get)
top_bandwidth = bandwidth_usage[top_bandwidth_user]

# Get the top remote host
remote_hosts = set()
for packet in packets:
    source_ip, dest_ip = re.findall(ip_pattern, packet)[0]
    if source_ip == top_bandwidth_user:
        remote_hosts.add(dest_ip)
top_remote_host = ', '.join(remote_hosts)

# Calculate the total bandwidth usage
total_bandwidth = sum(bandwidth_usage.values())

# Print the results
print("Top Bandwidth User:", top_bandwidth_user)
print("Top Remote Host:", top_remote_host)
print("Total Bandwidth Usage:", total_bandwidth)
