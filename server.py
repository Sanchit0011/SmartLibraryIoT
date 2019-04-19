# socket progrem test
#  create a socket object using socket.socket()
# for TCP pecify the socket type as socket.SOCK_STREAM. 
# User Datagram Protocol (UDP) sockets created with socket.SOCK_DGRAM
#  AF_INET is the Internet address family for IPv4
# Port to listen on (non-privileged ports are > 1023)
# listen() has a backlog parameter. It specifies the number of unaccepted connections that 

import socket
import json


class server():

    def servListen(self):
        HOST = ""
        PORT = 65000
        ADDRESS = (HOST, PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(ADDRESS)
            s.listen()
            while True:
                print("Now listening...\n")
                conn, addr = s.accept()
                print("Connected to {}".format(addr))
                data = conn.recv(4096)
                if not data:
                    break
                elif data == 'killsrv':
                    conn.close()
                    sys.exit()
                else:
                    data = data.decode()
                    loaded_data = json.loads(data)
                    x = loaded_data["username"]
                    
                    conn.sendall(data.encode())
                    print(x)
    
            
 
p = server()
p.servListen()


