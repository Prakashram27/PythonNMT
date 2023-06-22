import socket

def get_internal_hosts():
    hostname = socket.gethostname()
    local_ips = socket.gethostbyname_ex(hostname)[2]
    return local_ips

# Call the get_internal_hosts() function to retrieve the internal host IP addresses
internal_hosts = get_internal_hosts()
print(internal_hosts)
