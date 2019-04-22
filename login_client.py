import json
import socket
import time


class client():

    def clPost(self, ip):
        HOST = ip
        PORT = 65000
        ADDRESS = (HOST, PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect(ADDRESS)
            msg = "killsrv"
            s.sendall(msg.encode())
            s.close()
