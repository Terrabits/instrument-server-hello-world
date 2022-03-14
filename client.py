from socket import socket


# constants
SERVER_ADDRESS = ('localhost', 9000)

# connect
client = socket()
client.connect(SERVER_ADDRESS)

# get id_string
client.sendall(b'id_string?\n')
id_string = client.recv(1024)

# print
print('id_string?')
print(id_string.strip().decode())
