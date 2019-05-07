from psql import dbCon

# due date 1 week from borrow
# borrowed book can bot be borrowed
# when borrowed return event added to google calender


class borrow():
   """[summary]
   """

    def __init__(self, username, bookid):
        """Borrow class will use username and bookid to execute its methods
        
        Arguments:
            username {String} -- username of the user
            bookid {String} -- Unique book id of the book which is desired for borrowing
        """
        self.uname = username
        self.bkid = bookid

    def bkcheckout(self):
        """ function will perform logical checks before running the borrow querry

        """
        # check book is already borrowed or not
        q = ("""Select *
        from bookborrowed
        where lmsuserid like %s """)

        qBrw = (
            """ INSERT INTO bookborrowed (bookborrowedid, lmsuserid, bookid,
            status, borroweddate, returneddate)
            VALUES (default, %s, %s, 'borrowed',
            current_date, current_date + INTERVAL '7' DAY)""")

        rows = dbCon().selectQ(q, self.uname)
        print(rows)
        print(len(rows))
        if len(rows) is not 0:
            for r in rows:
                if r[2] is self.bkid:
                    q2Chk = ("""Select *
                    from bookborrowed
                    where lmsuserid like %s AND bookid=%s
                    ORDER BY bookborrowedid DESC
                    LIMIT 1 """)
                    userRows = dbCon().selectQ(q2Chk, self.uname, self.bkid)
                    print(userRows)
                    for i in userRows:
                        if i[3] is "returned":
                            # user can borrow book,borrow querry
                            dbCon().insUpDel(qBrw)

                        else:
                            # user can not borrow book,reject Alert
                            print("Book already borrowed")

        else:
            # borrow book since this book was never borrowed or
            # returned,borrow book
            dbCon().insUpDel(qBrw, self.uname, self.bkid)
            print("Book borrow sucessfull")

        #     p


p = borrow("halil", 4)
p.bkcheckout()
