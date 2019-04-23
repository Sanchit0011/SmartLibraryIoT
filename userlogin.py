# Imported the necessary modules
import sys
import sqlite3
import os
import re
import socket
import json
from login_client import login
from server import server


# Defined the userlogin class
class userlogin:

    # Function to establish database connection
    def create_conn(self):
        path1 = os.path.realpath(__file__)
        path2 = os.path.basename(__file__)
        rel_path = path1.replace(path2, "")

        conn = sqlite3.connect(rel_path + 'PIoT_db2.db')
        return(conn)

    # Function to display user login menu and
    # perform action based on user choice
    def createloginMenu(self):

        while(1):
            # Displaying user login menu
            print()
            print('Please select the option you want to proceed with:')
            print()
            print('1. Register new user')
            print('2. Log in to system')
            print('3. exit')
            print()

            # Took user option as input
            options = input()
            if(options != '1' and options != '2' and options != '3'):
                print()
                print('Please enter 1 or 2 as your choices')

            # If option 1 then register new user
            elif(options == '1'):

                # Created userdetails table in database
                conn = self.create_conn()
                cur = conn.cursor()
                conn.execute('''CREATE TABLE IF NOT EXISTS USERDETAILS
                ( USERID TEXT PRIMARY KEY,
                PASSWORD TEXT NOT NULL,
                FIRSTNAME TEXT NOT NULL,
                LASTNAME TEXT NOT NULL,
                EMAIL TEXT NOT NULL
                );''')

                # Input and validate username
                flag = True
                while(flag):
                    print()
                    username = input('Enter username: ')
                    cur.execute('''SELECT USERID from USERDETAILS
                    where USERID=?''', (username,))
                    data = cur.fetchall()
                    if len(data) >= 1:
                        print()
                        print('Username already exists')
                    elif(len(username) is 0):
                        print()
                        print('Please enter Username in correct format')
                    else:
                        flag = False

                # Input and validate first name
                while(flag is False):
                    print()
                    firstName = input('Enter first name: ')
                    match = bool(re.match('^[a-zA-Z\s]*$', firstName))
                    if(match is False or len(firstName) is 0):
                        print()
                        print('Please enter first name in correct format')
                    else:
                        flag = True

                # Input and validate last name
                while(flag):
                    print()
                    lastName = input('Enter last name: ')
                    match = bool(re.match('^[a-zA-Z\s]*$', lastName))
                    if(match is False or len(firstName) is 0):
                        print()
                        print('Please enter last name in correct format')
                    else:
                        flag = False

                # Input and validate e-mail
                while(flag is False):
                    print()
                    email = input('Enter e-mail: ')
                    match = bool(re.match('[^@]+@[^@]+\.[^@]+', email))
                    cur.execute('''SELECT EMAIL from USERDETAILS
                    where EMAIL=?''', (email,))
                    data = cur.fetchall()
                    if(match is False or len(firstName) is 0):
                        print()
                        print('Please enter e-mail in correct format')

                    elif(len(data) >= 1):
                        print()
                        print('This e-mail has already been registered')
                    else:
                        flag = True

                # Input and validate password
                while(flag):
                    print()
                    passw = input('Enter password: ')
                    passlen = len(passw)
                    regexstr = '(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)'
                    match = bool(re.match(regexstr, passw))
                    if(passlen < 8 or match is False):
                        errorstr = 'Password should be atleast 8 characters'
                        errorstr = errorstr + ' containing uppercase letter,'
                        errorstr = errorstr + ' lowercase letter,'
                        errorstr = errorstr + ' digit and symbol'
                        print()
                        print(errorstr)
                    else:
                        # If all details valid then insert into table
                        conn.execute('''INSERT INTO USERDETAILS
                        (USERID, PASSWORD,
                        FIRSTNAME,
                        LASTNAME, EMAIL) \
                            VALUES(?, ?, ?,
                            ?, ?);
                            ''', (username, passw, firstName, lastName, email))
                        conn.commit()
                        conn.close()
                        break

            # If option 2 then log in to system
            elif(options == '2'):

                # Create connection to db
                conn = self.create_conn()
                cur = conn.cursor()
                print()

                # Input username and password
                uname = input('Enter username: ')
                passw = input('Enter password: ')
                cur.execute('''SELECT userid,password from USERDETAILS
                where userid = ? and password = ?''', (uname, passw,))
                credentials = cur.fetchall()

                # If username and password exist, run client and server code
                if(len(credentials) >= 1):
                    print()

                    # Client code to send login success message to master pi
                    HOST = input("input server ip ")
                    print()
                    print("Login successful!")
                    PORT = 65000
                    ADDRESS = (HOST, PORT)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.connect(ADDRESS)
                    msgdict = {"username": uname, "status": 'success'}
                    msg = json.dumps(msgdict)
                    s.sendall(msg.encode())

                    # Server code to receive logout message from master pi
                    HOST = ""
                    ADDRESS = (HOST, PORT)
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(ADDRESS)
                    s.listen()
                    while True:
                        print("Waiting for user logout...\n")
                        con, addr = s.accept()
                        print(uname + ", you have logged out")
                        data = con.recv(4096)
                        data = data.decode()
                        if not data:
                            break
                        elif data == 'killsrv':
                            con.close()
                            break
                else:
                    print()
                    print('Credentials are not valid!')

            # If option 3 then exit system
            elif(options == '3'):
                sys.exit(0)

# Created loginMenu object and called createloginMenu()
ul = userlogin()
ul.createloginMenu()
