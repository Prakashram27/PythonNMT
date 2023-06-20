import re
import subprocess
import threading
import time
from collections import Counter

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+) Bytes\)'

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

    ip_matches = re.findall(ip_pattern, output)
    usage_matches = re.findall(usage_pattern, output)

    ip = [match[0] for match in ip_matches]
    usage = [match for match in usage_matches]

    calling_function(ip, usage)
    usage_data.extend((ip_address, dest_ip, int(packet_length)) for ip_address, dest_ip, packet_length in zip(ip, usage))

def calculations():
    global usage_data, total_usage, top_users
    total_usage = sum(packet_length for _, _, packet_length in usage_data)
    user_counts = Counter(ip_address for ip_address, _, _ in usage_data)
    top_users = user_counts.most_common(5)

def capture_output(process):
    for line in process.stdout:
        output = line.decode().strip()
        process_output(output)

#Starts here 
command = "sudo netsniff-ng -i wlp2s0"

process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

output_thread = threading.Thread(target=capture_output, args=(process,))
output_thread.start()

# Start time for 30-second interval
start_time = time.time()

while True:
    if time.time() - start_time >= 30:
        calculations()
        print("Total Usage:", total_usage)

        print("Top 5 Users:")
        for user, count in top_users:
            print(f"User: {user}, Usage: {count} packets")

        
        #resetting here
        usage_data.clear()
        start_time = time.time()

process.wait()
output_thread.join()


return_code = process.returncode
print("Return Code:", return_code)
