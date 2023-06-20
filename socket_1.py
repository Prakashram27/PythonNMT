# import socket

# def scan_port(host, port):
#     try:
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.settimeout(2)  # Adjust the timeout as needed
#         sock.connect((host, port))
#         print(f"Port {port} is open")
#     except socket.error:
#         print(f"Port {port} is closed")
#     finally:
#         sock.close()

# def scan_host(host, start_port, end_port):
#     print(f"Scanning host: {host}")
#     for port in range(start_port, end_port + 1):
#         scan_port(host, port)

# # Example usage
# scan_host("127.0.0.1", 1, 1000)