from psql import dbCon

# due date 1 week from borrow
# borrowed book can bot be borrowed
# when borrowed return event added to google calender


class borrow():

    def __init__(self, username, bookid):
        """Borrow class will use username and bookid to execute its methods

        Arguments:
            username {String} -- username of the user
            bookid {String} -- Unique book id of the book
            which is desired for borrowing
        """
        self.uname = username
        self.bkid = bookid

    def bkcheckout(self):
        """ function will perform logical checks before running the borrow querry

        """
        # check book is already borrowed or not
        q = ("""Select *
        from bookborrowed
        where bookid = %s """)

        qBrw = (
            """ INSERT INTO bookborrowed (bookborrowedid, lmsuserid, bookid,
            status, borroweddate, returneddate)
            VALUES (default, %s, %s, 'borrowed',
            current_date, null)""")

        rows = dbCon().selectQ(q, self.bkid)
        if len(rows) is not 0:
            for r in rows:
                if r[2] - self.bkid is 0:
                    q2Chk = ("""Select *
                    from bookborrowed
                    where bookid = %s
                    ORDER BY bookborrowedid DESC
                    LIMIT 1 """)
                    userRows = dbCon().selectQ(q2Chk, self.bkid)
                    if userRows[0][3][0] is 'r':
                        # user can borrow book,borrow querry
                        dbCon().insUpDel(qBrw, self.uname, self.bkid)
                        print("Book borrow sucessfull")
                    else:
                        # user can not borrow book,reject Alert
                        print("Book already borrowed")
                        break

        else:
            # borrow book since this book was never borrowed or
            # returned,borrow book
            dbCon().insUpDel(qBrw, self.uname, self.bkid)
            print("Book borrow sucessfull")
