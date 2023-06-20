import re
import subprocess
import threading

ip_pattern = r'IPv4 Addr \(([\d.]+) => ([\d.]+)\)'
usage_pattern = r'Len \((\d+) Bytes'




array = """ """


def calling_function(ip,usage):
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',len(ip))
    print(len(usage))
    for i in range(min(len(ip), len(usage))):
        ip_address = ip[i][0]
        dest_ip = ip[i][1]
        packet_length = usage[i]
        print(f'"IP Address:", {ip_address} => "Destination IP",{dest_ip} ,"Packet Length:", {packet_length}')
        print("-----------------------------------------------------------------------------------------------")

def process_output(output):
    # Processcla each line of the output
    # Perform any necessary parsing or processing here
    # print(output.strip())
    global array
    array += output
    # print(array)
    # print('----------------------------------------------------------------------------------',len(array))

    ip = re.findall(ip_pattern,array)
    usage = re.findall(usage_pattern,array)
    calling_function(ip,usage)

        # print('stoped')
        # 
    # Wait for the output thread to finish
        # output_thread.join()
def capture_output(process):
    # Read the output of the process in real-time
    for line in process.stdout:
        output = line.decode().strip()
        process_output(output)

command = "sudo netsniff-ng -i wlp2s0"

# Create a new process for the command
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Create a thread to capture the output
output_thread = threading.Thread(target=capture_output, args=(process,))
output_thread.start()

# Do other work here
# You can perform any other tasks while the process is running and the output is being captured

# Wait for the process to complete
# process.wait(30)

# Join the output thread to wait for it to finish
output_thread.join()

# Retrieve the return code
return_code = process.returncode

# Print the return code
print("Return Code:>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", return_code)