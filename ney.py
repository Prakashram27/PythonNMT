import re
from collections import defaultdict

# Regex patterns to extract relevant information
# packet_pattern = r'> (\w+) \d+ \d+s\.\d+ns #\d+'
# ip_pattern = r'IPv4 Addr \((.*?) => (.*?)\)'
# data_off_pattern = r'DataOff \((\d+)\)'
# length_pattern = r'Len \((\d+)\)'

packet_pattern = r'> (\w+) \d+ \d+s\.\d+ns #\d+'
# ip_pattern = r'IPv4 Addr \((.*?) => (.*?)\)'
ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'

data_off_pattern = r'DataOff \((\d+)\)'
length_pattern = r'Len \((\d+)\)'




# Dictionary to store bandwidth usage for each IP
bandwidth_usage = defaultdict(int)
print(bandwidth_usage)

# Extract information from each packet
packets = re.findall(packet_pattern, output)
print(packets)

ip_matches = re.findall(ip_pattern, packet)
if ip_matches:
        source_ip, dest_ip = ip_matches[0]
        print("Source IP:", source_ip)
        print("Destination IP:", dest_ip)
else:
        print("No IP addresses found in the packet.")
# for packet in packets:
#     source_ip, dest_ip = re.findall(ip_pattern, packet)[0]
#     data_offset = int(re.findall(data_off_pattern, packet)[0])
#     packet_length = int(re.findall(length_pattern, packet)[0])
#     bandwidth_usage[source_ip] += packet_length - data_offset

# Check if bandwidth_usage is empty
if not bandwidth_usage:
    print("No packets found.")
    exit()

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









# pandas

import pandas
import glob

file_path = '*.xlsx'
data = []

for file in glob.glob(file_path):
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(file, sheet_name=sheet_name, usecols=[0])
        data.append(df)
merged_data = pd.concat(data, axis=0)
total = merged_data.sum()

output_file = 'output.xlsx'
with pd.ExcelWriter(output_file) as writer:
    total.to_excel(writer, sheet_name='Total', index=False)