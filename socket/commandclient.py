import socket

# Initialize client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('rcpi', 9999))

while True:
    client_socket.send((input()+"\n").encode())
