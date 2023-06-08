# import socket

# HOST = "127.0.0.1"  # The server's hostname or IP address
# PORT = 8000  # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b"Hello, world")
#     data = s.recv(1024)

# print(f"Received {data!r}")

"""shell_client.py for python3.  Read data from a socket and, read a command from stdin, and send the command over the socket."""

import socket
import time

import bufsock

# Give the server time to start up.
time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# We use port 4444 so we don't need to be root to run this.
s.connect(("192.168.223.100", 8080))
bs = bufsock.bufsock(s)

while True:
    # Read the prompt and print it.
    data = bs.readto(b'\n')
    print(data)
    # Read a command from the user's terminal.
    cmd = input()
    # Send the command to the server, terminated with a newline.
    bs.send(cmd.encode('utf-8'))
    bs.send(b'\n')
    bs.flush()
    # Read the command's always-one-line response and print it.
    data = bs.readto(b'\n')
    print(data)