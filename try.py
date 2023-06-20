import re
import subprocess
import threading
import time
from collections import Counter

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+) Bytes'

usage_data = []
total_usage = []
top_users = []

def calling_function(ip, usage):
    for i in range(min(len(ip), len(usage))):
        ip_address = ip[i][0]
        dest_ip = ip[i][1]
        packet_length = int(usage[i])
        print(f"IP Address: {ip_address} => Destination IP: {dest_ip}, Packet Length: {packet_length}")

def process_output(output):
    global usage_data, total_usage, top_users

    ip = re.findall(ip_pattern, output)
    usage = re.findall(usage_pattern, output)
    calling_function(ip, usage)

    # Adding usage 
    usage_data.extend((ip_address, dest_ip, int(packet_length)) for ip_address, dest_ip, packet_length in zip(ip, usage))
    total_usage.extend(int(packet_length) for _, _, packet_length in zip(ip, usage))

    # Calculate the top 5 users by usage
    user_counts = Counter(ip)
    top_users = user_counts.most_common(5)

def capture_output(process):
    for line in process.stdout:
        output = line.decode().strip()
        process_output(output)

# Command to execute
command = "sudo netsniff-ng -i wlp2s0"

# Create a new process for the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create a thread to capture the output
output_thread = threading.Thread(target=capture_output, args=(process,))
output_thread.start()

# Start time for 30-second interval
start_time = time.time()

while True:
    # Check if 30 seconds have passed
    if time.time() - start_time >= 30:
        # Perform any calculations or processing on the collected data
        print("Total Usage:", sum(total_usage), "bytes")

        print("Top 5 Users:")
        for user, count in top_users:
            print(f"User: {user}, Usage: {count} packets")

        # Clear the data for the next 30-second interval
        usage_data.clear()
        total_usage.clear()
        top_users.clear()

        # Reset the start time for the next 30-second interval
        start_time = time.time()

    # Continue with other work or tasks here

# Wait for the process to complete
process.wait()

# Join the output thread to wait for it to finish
output_thread.join()

# Retrieve the return code
return_code = process.returncode

# Print the return code
print("Return Code:", return_code)
