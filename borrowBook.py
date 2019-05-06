from psql import dbCon

# due date 1 week from borrow
# borrowed book can bot be borrowed
# when borrowed return event added to google calender
# INSERT INTO public."Cakesandwich" (name, status) SELECT $1, $2 WHERE NOT EXISTS
# ( SELECT Count(lmsuserid)
# FROM bookborrowed
# WHERE lmsusernameid like %s And status like 'borrowed' And bookid like %s)
# SELECT Count(lmsuserid) FROM bookborrowed WHERE lmsusernameid like %s
# And status like 'borrowed' And bookid like %s


class borrow():
    def __init__(self, username, bookid):
        self.username = username
        self.bookid = bookid

    def bkcheckout(self):
        # check book is already borrowed or not
        q = ("""Select *
        from bookborrowed
        where lmsuserid like %s """)

        qBrw = (
            """ INSERT INTO bookborrowed (bookborrowedid, lmsuserid, bookid,
            status, borroweddate, returneddate)
            VALUES (default, %s, %s, 'borrowed',
            current_date, current_date + INTERVAL '7' DAY)""")

        rows = dbCon().selectQ(q, self.username)
        print(rows)
        for r in rows:
            if r[2] is self.bookid:
                q2Chk = ("""Select *
                from bookborrowed
                where lmsuserid like %s AND bookid is like %s
                ORDER BY bookborrowedid DESC
                LIMIT 1 """)
                userRows = dbCon().selectQ(q2Chk, self.username, self.bookid)

                if userRows[3] is "returned":
                    # user can borrow book,borrow querry
                    dbCon().insUpDel(qBrw)

                else:
                    # user can not borrow book,reject Alert
                    print("Book already borrowed")

            else:
                # borrow book since this book was never borrowed or
                # returned,borrow book
                dbCon().insUpDel(qBrw, self.username, self.bookid)
                print("Book borrow sucessfull")

        #     p


p = borrow("kashif1", 432)
p.bkcheckout()
