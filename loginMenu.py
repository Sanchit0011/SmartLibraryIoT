import sys
import sqlite3
import os
import re


class loginMenu:

    def create_conn(self):
        path1 = os.path.realpath(__file__)
        path2 = os.path.basename(__file__)
        rel_path = path1.replace(path2, "")

        conn = sqlite3.connect(rel_path + 'PIoT_db2.db')
        return(conn)

    def createloginMenu(self):

        while(1):
            print()
            print('Please select the option you want to proceed with:')
            print()
            print('1. Register new user')
            print('2. Log in to system')
            print('3. exit')
            print()

            options = input()
            if(options != '1' and options != '2' and options != '3'):
                print()
                print('Please enter 1 or 2 as your choices')

            elif(options == '3'):
                sys.exit(0)

            elif(options == '1'):

                conn = self.create_conn()
                cur = conn.cursor()
                conn.execute('''CREATE TABLE IF NOT EXISTS USERDETAILS
                ( USERID TEXT PRIMARY KEY,
                PASSWORD TEXT NOT NULL,
                FIRSTNAME TEXT NOT NULL,
                LASTNAME TEXT NOT NULL,
                EMAIL TEXT NOT NULL
                );''')

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
                    else:
                        flag = False

                while(flag is False):
                    print()
                    firstName = input('Enter first name: ')
                    match = bool(re.match('^[a-zA-Z\s]*$', firstName))
                    if(match is False):
                        print()
                        print('Please enter first name in correct format')
                    else:
                        flag = True

                while(flag):
                    print()
                    lastName = input('Enter last name: ')
                    match = bool(re.match('^[a-zA-Z\s]*$', lastName))
                    if(match is False):
                        print()
                        print('Please enter last name in correct format')
                    else:
                        flag = False

                while(flag is False):
                    print()
                    email = input('Enter e-mail: ')
                    match = bool(re.match('[^@]+@[^@]+\.[^@]+', email))
                    cur.execute('''SELECT EMAIL from USERDETAILS
                    where EMAIL=?''', (email,))
                    data = cur.fetchall()
                    if(match is False):
                        print()
                        print('Please enter e-mail in correct format')

                    elif(len(data) >= 1):
                        print()
                        print('This e-mail has already been registered')
                    else:
                        flag = True

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

lm = loginMenu()
lm.createloginMenu()
