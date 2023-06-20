import subprocess
import re




input_data = """< enp1s0 66 1686655580s.523649734ns #114
[ Eth MAC (e4:b3:18:dd:8e:ac => 00:a0:c9:4c:60:92), Proto (0x0800, IPv4) ]
[ Vendor (Unknown => INTEL CORPORATION - HF1-06) ]
[ IPv4 Addr (192.168.0.151 => 192.168.0.104), Proto (6), TTL (64), TOS (16), Ver (4), IHL (5), Tlen (52), ID (41325), Res (0), NoFrag (1), MoreF rag (0), FragOff (0), CSum (0x16f7) is ok ]
[ TCP Port (37290 => 5000 (upnp)), SN (0xe1020328), AN (0xaeb03cb1), DataOff (8), Res (0), Flags (ACK), Window (5719), CSum (0x2b2d), Ur gPtr (0) ]
[ Chr .....Tpw..N. ]
[ Hex 01 01 08 0a ad 54 70 77 d1 b5 4e a8 ]

> enp1s0 102 1686655580s.523704982ns #115
[ Eth MAC (00:a0:c9:4c:60:92 => e4:b3:18:dd:8e:ac), Proto (0x0800, IPv4) ]
[ Vendor (INTEL CORPORATION - HF1-06 => Unknown) ]
[ IPv4 Addr (192.168.0.11 => 192.168.0.300), Proto (6), TTL (64), TOS (16), Ver (4), IHL (5), Tlen (88), ID (54649), Res (0), NoFrag (1), MoreF rag (0), FragOff (0), CSum (0xe2c6) is ok ]
[ TCP Port (5000 (upnp) => 37290), SN (0xaeb03f11), AN (0xe1020328), DataOff (8), Res (0), Flags (PSH ACK), Window (43), CSum (0x829a), UrgPtr (0) ]
[ Chr ......N^C.Tpw........>.f.r..Q..@..?...h...j.>.a*. ]
[ Hex 01 01 08 0a d1 b5 4e a9 ad 54 70 77 fb dc 0c c2 a0 8a 82 f8 3e 10 66



"""


def extract_values(line):
    source_ip_match = re.search(r"IPv4 Addr \((.*?) =>", line)
    print(1)
    source_ip = source_ip_match.group(1) if source_ip_match else None

    dest_ip_match = re.search(r"=> (.*?),", line)
    dest_ip = dest_ip_match.group(1) if dest_ip_match else None
    print(2)


    bandwidth_match = re.search(r"Tlen \((\d+)", line)
    bandwidth = int(bandwidth_match.group(1)) if bandwidth_match else None
    print(3)

    print(source_ip,dest_ip,bandwidth)

    return source_ip, dest_ip, bandwidth

# Run the 'netsniff-ng' command as a subprocess and capture its output
process = subprocess.Popen(['netsniff-ng', '-i', 'enp1s0', '-o', 'x'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Continuously process and print the extracted values from real-time data
while True:
    line = process.stdout.readline().decode().strip()
    
    if not line:
        break

    source_ip, dest_ip, bandwidth = extract_values(line)
    print()

    if source_ip:
        print(f"Source IP: {source_ip}, Dest IP: {dest_ip}, Bandwidth: {bandwidth}")

extract_values(input_data)






# output = """
# M wlp2s0 214 1686723548s.456661878ns #27 
#  [ Eth MAC (1a:c9:44:25:4d:77 => 01:00:5e:00:00:fb), Proto (0x0800, IPv4) ]
#  [ Vendor (Locally Administered => Multicast) ]
#  [ IPv4 Addr (192.168.0.72 => 224.0.0.251), Proto (17), TTL (255), TOS (0), Ver (4), IHL (5), Tlen (200), ID (56775), Res (0), NoFrag (0), MoreFr
#    ag (0), FragOff (0), CSum (0x3b71) is ok ]
#  [ UDP Port (5353 (zeroconf) => 5353 (zeroconf)), Len (180 Bytes, 172 Bytes Data), CSum (0xbaf2) ]
#  [ Chr .............Sabarish...s iPhone._rdlink._tcp.local......Sabarishs-iPhone.-.......!.....x.........8.8.......x............<Q.<...8.......x.
#    ....H..)................Gla...D%Mw ]
#  [ Hex  00 00 00 00 00 02 00 00 00 03 00 01 13 53 61 62 61 72 69 73 68 e2 80 99 73 20 69 50 68 6f 6e 65 07 5f 72 64 6c 69 6e 6b 04 5f 74 63 70 05
#    6c 6f 63 61 6c 00 00 ff 00 01 10 53 61 62 61 72 69 73 68 73 2d 69 50 68 6f 6e 65 c0 2d 00 ff 00 01 c0 0c 00 21 00 01 00 00 00 78 00 08 00 00 0
#    0 00 c0 02 c0 38 c0 38 00 1c 00 01 00 00 00 78 00 10 fe 80 00 00 00 00 00 00 1c 80 3c 51 e1 3c e3 d5 c0 38 00 01 00 01 00 00 00 78 00 04 c0 a8
#    00 48 00 00 29 05 a0 00 00 11 94 00 12 00 04 00 0e 00 9a ba 90 47 6c 61 13 1a c9 44 25 4d 77 ]

# M wlp2s0 259 1686723548s.456661323ns #25 
#  [ Eth MAC (1e:9e:bd:96:e1:54 => 01:00:5e:00:00:fb), Proto (0x0800, IPv4) ]
#  [ Vendor (Locally Administered => Multicast) ]
#  [ IPv4 Addr (192.168.0.52 => 224.0.0.251), Proto (17), TTL (255), TOS (0), Ver (4), IHL (5), Tlen (245), ID (37667), Res (0), NoFrag (0), MoreFr
#    ag (0), FragOff (0), CSum (0x85fc) is ok ]
#  [ UDP Port (5353 (zeroconf) => 5353 (zeroconf)), Len (225 Bytes, 217 Bytes Data), CSum (0xcb6a) ]
#  [ Chr .............6.3.5.C.0.A.4.A.9.2.C.A.0.2.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.E.F.ip6.arpa........x...Rajesh-iphone.local..52.0.168.192.in-addr
#    .P.......x...`.../.....x.........u./.....x...u......).............T..\..8.....T ]
#  [ Hex  00 00 84 00 00 00 00 02 00 00 00 03 01 36 01 33 01 35 01 43 01 30 01 41 01 34 01 41 01 39 01 32 01 43 01 41 01 30 01 32 01 30 01 30 01 30
#    01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 30 01 38 01 45 01 46 03 69 70 36 04 61 72 70 61 00 00 0c 80 01 00 00 00 7
#    8 00 15 0d 52 61 6a 65 73 68 2d 69 70 68 6f 6e 65 05 6c 6f 63 61 6c 00 02 35 32 01 30 03 31 36 38 03 31 39 32 07 69 6e 2d 61 64 64 72 c0 50 00
#    0c 80 01 00 00 00 78 00 02 c0 60 c0 0c 00 2f 80 01 00 00 00 78 00 06 c0 0c 00 02 00 08 c0 75 00 2f 80 01 00 00 00 78 00 06 c0 75 00 02 00 08 0
#    0 00 29 05 a0 00 00 11 94 00 12 00 04 00 0e 00 54 e2 92 5c 88 1b 38 1e 9e bd 96 e1 54 ]
# """

# command = f'sudo netsniff-ng'
# sudo_password = 'Prakash@123'
# output = subprocess.Popen(command.split(),universal_newlines=True,stdout=subprocess.PIPE)
# # cmd1 = subprocess.Popen(['echo', Prakash@123 ], stdout=subprocess.PIPE)
# print('success')
# print(output.stdout)


# command = 'sudo netsniff-ng'
# sudo_password = 'Prakash@123'
# process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
# output, error = process.communicate(input=sudo_password)
# print(process.stdout)


# command = 'sudo netsniff-ng'
# output = subprocess.check_output(command.split(), universal_newlines=True, input='Prakash@123\n', stderr=subprocess.DEVNULL)


# ip = re.findall(ip_pattern,output)
# print(ip)
# usage = re.findall(usage_pattern,output)
# print(usage)

# for i in range(min(len(ip), len(ip))):
#     ip_address = ip[i][0]
#     dest_ip = ip[i][1]
#     packet_length = usage[i]
#     print("IP Address:", ip_address)
#     print("Destination IP",dest_ip)
#     print("Packet Length:", packet_length)
#     print("-----------------------------------------------------------------------------------------------")


# Testing for subprocess 
# command = "ls -l"
# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# output, error = process.communicate()

# output = output.decode("utf-8")
# error = error.decode("utf-8")


# print("Output:")
# print(output)
# print("Error:")
# print(error)


# import subprocess

# # Command to execute
# command = "sudo netsniff-ng"

# # Create a new process for the command
# process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# # Read the output in real-time
# for line in process.stdout:
#     # Process each line of the output
#     # Here you can perform any necessary parsing or processing of the output
#     print(line.strip())

# # Wait for the process to complete
# process.wait()

# # Retrieve the return code
# return_code = process.returncode

# # Print the return code
# print("Return Code:", return_code)

