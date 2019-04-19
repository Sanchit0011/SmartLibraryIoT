# user login
import json
import socket
import time 


class login():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def connect(self):
        host = input("input server ip ")

        client().clPost(self.username, host, self.status)
        print(self.status)
        print(self.username)


class client():

    def clPost(self, name, ip, status):
        HOST = ip

        # HOST = "127.0.0.1" # The server's hostname or IP address.
        PORT = 65000         # The port used by the server.
        ADDRESS = (HOST, PORT)
        if status is "success":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Connecting to {}...".format(ADDRESS))
                s.connect(ADDRESS)
                print("Connected.")
                msgdict = {"username": name, "status": status}
                msg = json.dumps(msgdict)

                s.sendall(msg.encode())
                
                data = s.recv(4096)
                
                print("Received {}'".format(data.decode()))  # 
                return "user registered"
        else:
            print("user not registered")
            return "user not registered"
            

title = {'username': 'huzaifa123', 'status': 'success'}

p=login(**title)
p.connect()
