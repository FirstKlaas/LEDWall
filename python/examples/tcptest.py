import socket

b = bytearray(49*3)
b[0] = 243

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.8.70',3548))
s.send(b)
print('##############')
s.send(b)