import json
import socket
import time


class client():
    """logout from master pi
    """
    
    def clPost(self, ip):
        """send logout message over socket

        Arguments:
            ip {String} -- ip address to send logout message
        """
        HOST = ip
        PORT = 65000
        ADDRESS = (HOST, PORT)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect(ADDRESS)
        msg = "killsrv"
        s.sendall(msg.encode())
        s.close()
