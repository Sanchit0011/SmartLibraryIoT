import socket
import json
from login_client import client


class server():

    def servListen(self):
        # accept RP user username and success message
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            HOST = ""
            PORT = 65000
            ADDRESS = (HOST, PORT)
            s.bind(ADDRESS)
            s.listen()
            print("Waiting for user login...\n")
            conn, addr = s.accept()
            data = conn.recv(1024)
            data = data.decode()
            data = json.loads(data)
            print(data["username"] + " has successfuly logged in.")
            conn.close()
            while(True):
                print()
                print('Please select the option you want to proceed with:')
                print()
                print('1. Search a book')
                print('2. borrow a book')
                print('3. return a book')
                print('4. logout')
                print()
                # Took user option as input
                opt = input()
                if(opt != '1' and opt != '2' and opt != '3' and opt != '4'):
                    print()
                    print('Please enter 1,2,3 or 4 as your choices')

                elif(opt == '1'):
                    print("Enter book name to search")
                    bookNameToSearch = input()
                elif(opt == '2'):
                    print("Enter Book ID to borrow")
                    bookNameToBorrow = input()
                elif(opt == '3'):
                    print("Enter Book ID to return")
                    bookNameToReturn = input()
                elif(opt == '4'):
                    # send message to server for logout
                    client().clPost(addr[0])
                    print(data["username"] + " has successfuly logged out.")
                    print()
                    break


server().servListen()
