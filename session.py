import re
import subprocess
import threading
import time
from collections import Counter

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+)\)'

usage_data = []
total_usage = []
total_hosts = []
total_remote_hosts = []
lock = threading.Lock()

def calling_function(ip, usage):
    for i in range(min(len(ip), len(usage))):
        ip_address = ip[i][0]
        dest_ip = ip[i][1]
        packet_length = int(usage[i])
        usage_data.append((ip_address, dest_ip, packet_length))

def process_usage_data():
    top_users = Counter()
    top_hosts = Counter()
    print(usage_data)

    for ip_address, dest_ip, packet_length in usage_data:
        top_users[ip_address] += packet_length
        top_hosts[dest_ip] += packet_length

    # Get the top users and top remote hosts
    top_users = top_users.most_common(5)
    top_hosts = top_hosts.most_common(5)

    # Print the results   
    #  print("Top Users:")
    for user, usage in top_users:
        print(f"User: {user}, Usage: {usage} bytes")

    # print("Top Remote Hosts:")
    for host, usage in top_hosts:
        print(f"Host: {host}, Usage: {usage} bytes")

    print("Total Usage:", sum(total_usage), "bytes")

def process_output(output, start_time):
    global usage_data

    ip = re.findall(ip_pattern, output)
    usage = re.findall(usage_pattern, output)
    calling_function(ip, usage)

    # Check if 30 seconds have passed
    
    process_usage_data()
    usage_data = []
    start_time = time.time()

def capture_output(process):
    start_time = time.time()

    for line in process.stdout:
        output = line.decode().strip()
        process_output(output, start_time)

# Command to execute
command = "sudo netsniff-ng -i wlp2s0"

# Create a new process for the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create a thread to capture the output
output_thread = threading.Thread(target=capture_output, args=(process,))
output_thread.start()

# Wait for the process to complete
process.wait()

# Join the output thread to wait for it to finish
output_thread.join()

# Retrieve the return code
return_code = process.returncode

# Print the return code
print("Return Code:", return_code)