import socket
import json
from logout_client import client
from psql import dbCon
from borrowBook import borrow
from returnBook import Return


class server():
    """class to recieve connection from RP through socket and provide library functions
    """
    def checkBID(self, bid):
        """check if book ID is in list of books
        
        Arguments:
            bid {int} -- book id to check
        """
        qu = ("""select bookid
            from book
            """)
        bIDs = dbCon().selectQ(qu)
        bIDList = []
        for ids in bIDs:
            bIDList.append(ids[0])
        if bid in bIDList:
            return True
        else:
            return False

    def servListen(self):
        """display library menu and call return borrow and search book.
        """
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
            conn.close()
            uname = data["username"]
            fname = data["fname"]
            lname = data["lname"]
            uEmail = data["email"]
            uid = -1
            row = dbCon().selectQ("""
            select uname, lmsuserid, lmsuserid-lmsuserid+1
            from lmsuser where uname = %s ;
            """, uname)
            flag = True
            register = True
            if len(row) > 0:
                if(row[0][2] is 1):
                    flag = True
                    uid = row[0][1]
                    print("user found")
            else:
                flag = False
                row = dbCon().insUpDel("""
                INSERT INTO lmsuser(
                lmsuserid, firstname, lastname, email, uname)
                VALUES (default, %s, %s, %s, %s);
                """, fname, lname, uEmail, uname)
                row = dbCon().selectQ("""
                SELECT lmsuserid
                FROM lmsuser
                where uname = %s;
                """, uname)
                uid = row[0][0]
                flag = True
                print("user registered")

            print(fname + " " + lname + " has successfuly logged in.")
            while(flag is True and uid > -1):
                print()
                print('Please select the option you want to proceed with:')
                print()
                print('1. Search a book')
                print('2. borrow a book')
                print('3. return a book')
                print('4. logout')
                print()
                opt = input()
                if(opt != '1' and opt != '2' and opt != '3' and opt != '4'):
                    print()
                    print('Please enter 1,2,3 or 4 as your choices')

                elif(opt == '1'):
                    print("Enter book name to search")
                    bookTitle = input()
                    q = ("""select distinct
                    book.bookid, book.title, book.author, book.publisheddate
                    from book
                    where title like %s """)
                    rows = dbCon().selectQ(q, "%"+bookTitle+"%")
                    print("| Bookid | Title | Author | Published Date |")
                    for r in rows:
                        print(str(r[0])+" | "+r[1]+" | "+r[2]+" | "+str(r[3]))
                elif(opt == '2'):
                    print("Enter Book ID to borrow")
                    bookID = input()
                    bookID = int(bookID)
                    if self.checkBID(bookID):
                        p = borrow(uid, bookID)
                        p.bkcheckout()
                    else:
                        print("Invalid book ID")
                elif(opt == '3'):
                        p = Return(uid)
                        p.returnBook()
                elif(opt == '4'):
                    client().clPost(addr[0])
                    print(fname + " " + lname + " has successfuly logged out.")
                    uname = ""
                    fname = ""
                    lname = ""
                    uEmail = ""
                    uid = -1
                    print()
                    break
server().servListen()
