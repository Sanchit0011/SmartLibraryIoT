
# AF_INET is the Internet address family for IPv4


import socket
import json


class server():

    def servListen(self):
        HOST = ""
        PORT = 65000        # Port to listen on (non-privileged ports are > 1023)
        ADDRESS = (HOST, PORT)          ##  create a socket object using socket.socket(),socket.SOCK_STREAM for TCP
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


