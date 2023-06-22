import subprocess
import time
import pprint

def get_network_hosts():
    command = "nmap -sn --open --unprivileged 192.168.0.0/23 | grep 'Nmap scan report' | awk '{print $NF}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()



    output = output.decode("utf-8")   # Decode the output from bytes to string
    lines = output.splitlines() # Split the output into lines
    print(lines)
    #REturn
    return lines
start_time = time.time()
get_network_hosts()

end_time = time.time()

execution_time = end_time - start_time
pprint(f"{execution_time} seconds")