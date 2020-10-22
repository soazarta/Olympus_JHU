import select
import socket
import sys


HOST = "localhost"
PORT = 54321


def handle_data(s: socket.socket):
    """Handle all incoming and outgoing messages on the socket.

    Args:
        s (socket.socket): The socket to listen on
    """
    while True:
        rlist = [s, sys.stdin]
        readable, _ , _ = select.select(rlist, [], [])
        for r in readable:
            if r == s:
                data = r.recv(1024).decode()
                if data:
                    print(data)
                else:
                    r.close()
                    s.close()
                    exit(0)
            if r == sys.stdin:
                data = sys.stdin.readline()
                s.sendall(data.encode())


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Listen on our new socket
    handle_data(s)
