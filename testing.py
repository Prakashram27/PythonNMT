import re
import subprocess
import threading
import time

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+) Bytes'

array = ""

def calling_function(ip, usage):
    for i in range(min(len(ip), len(usage))):
        ip_address = ip[i][0]
        dest_ip = ip[i][1]
        packet_length = usage[i]
        print(f'IP Address: {ip_address} => Destination IP: {dest_ip}, Packet Length: {packet_length}')
        # print("-----------------------------------------------------------------------------------------------")

def process_output(output):
    global array
    array += output
    # Check if the output contains the required information
    if re.search(ip_pattern, array) and re.search(usage_pattern, array):
        ip = re.findall(ip_pattern, array)
        usage = re.findall(usage_pattern, array)
        calling_function(ip, usage)

def capture_output(process):
    # Read the output of the process in real-time
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

# Wait for 30 seconds
time.sleep(30)

# Terminate the process if it is still running
if process.poll() is None:
    process.terminate()

# Join the output thread to wait for it to finish
output_thread.join()

# Retrieve the return code
return_code = process.returncode

# Print the return code
print("Return Code:", return_code)
