import re
import subprocess
import threading
from collections import Counter
import time

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+) Bytes\)'

array = """"""
lock = threading.Lock()

def calling_function(ip, usage, usage_data):
    print('calling function started')
    for i in range(min(len(ip), len(usage))):
        ip_address = ip[i][0]
        dest_ip = ip[i][1]
        packet_length = int(usage[i])
        usage_data.append((ip_address, dest_ip, packet_length))

def process_usage_data(usage_data, total_usage, total_hosts, total_remote_hosts):
    top_users = Counter()
    top_hosts = Counter()

    for ip_address, dest_ip, packet_length in usage_data:
        top_users[ip_address] += packet_length
        top_hosts[dest_ip] += packet_length

    # Get the top users and top remote hosts
    top_users = top_users.most_common(10)
    top_hosts = top_hosts.most_common(10)

    # Print the results
    print("Top Users:")
    for user, usage in top_users:
        print(f"User: {user}, Usage: {usage} bytes")

    print("Top Remote Hosts:")
    for host, usage in top_hosts:
        print(f"Host: {host}, Usage: {usage} bytes")

    # Log the total usage, host, and remote host during the interval
    total_usage.extend(packet_length for _, _, packet_length in usage_data)
    total_hosts.append(len(set(ip_address for ip_address, _, _ in usage_data)))
    total_remote_hosts.extend(dest_ip for _, dest_ip, _ in usage_data)

    # Clear the usage data for the next interval
    usage_data.clear()

def process_output(output, usage_data, total_usage, total_hosts, total_remote_hosts, start_time):
    print('Process output started')
    global array
    array += output

    ip = re.findall(ip_pattern, array)
    usage = re.findall(usage_pattern, array)
    calling_function(ip, usage, usage_data)

    # Check if the interval has passed
    if time.time() - start_time >= 30:
        with lock:
            process_usage_data(usage_data, total_usage, total_hosts, total_remote_hosts)

        # Reset the start time and clear the array variable
        start_time = time.time()

    # Clear the array variable for the next interval

def capture_output(process, usage_data, total_usage, total_hosts, total_remote_hosts, start_time):
    print("capture output started......................................................")
    for line in process.stdout:
        print('forloop started inside the capture output')
        output = line.decode().strip()
        print('before process output')
        process_output(output, usage_data, total_usage, total_hosts, total_remote_hosts, start_time)

# Command to execute
command = "sudo netsniff-ng -i wlp2s0"

# Create a new process for the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create a thread to capture the output
usage_data = []
total_usage = []
total_hosts = []
total_remote_hosts = []
start_time = time.time()
output_thread = threading.Thread(target=capture_output, args=(process, usage_data, total_usage, total_hosts, total_remote_hosts, start_time))
output_thread.start()

while True:
    print('while')
    time.sleep(30)



