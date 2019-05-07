from psql import dbCon


class Return:
    def __init__(self, username):
        self.username = username

    def returnBook(self):
        b = ("""Select bookborrowed.bookid, title
        from bookborrowed inner join book 
        on bookborrowed.bookid = book.bookid
        where lmsuserid like %s and status = 'borrowed' """)

        qRtn = ("""UPDATE bookborrowed
        SET status = 'returned',
            returneddate = current_date
        where bookid = %s """)

        books = dbCon().selectQ(b, self.username)
        print("| Bookid | Title |")
        for r in books:
            print(str(r[0])+" | "+r[1])

        allBooks = ("""SELECT * FROM bookborrowed """)

        inputid = input("Enter the ID of the book you want to return: ")

        #check if the book has been borrowed
        bookRows = dbCon().selectQ(allBooks, self.username, inputid)
        print(bookRows)
        for i in bookRows:
            status = i[3][0]
            if status is 'b':
                dbCon().insUpDel(qRtn, inputid)
                print("Book return successful")

            else:
                print("The book has not been borrowed yet")
                 
p = Return("halil")
p.returnBook()
