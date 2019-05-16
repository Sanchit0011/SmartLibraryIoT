import pandas as pd
from psql import dbCon as psql
import numpy as np
import matplotlib.pyplot as plt
from datetime import *
import warnings

# Suppress all warnings
warnings.simplefilter(action='ignore')


class visual():

    def object_declare(self):
        obj = psql()
        return obj

    def foo(self, year, week):
        d = date(year, 1, 1)
        dlt = timedelta(days=(week-1)*7)
        return str(d + dlt) + " " + "-" + " " + str(d + dlt + timedelta(days=6))

    def create_day_graph(self):

        obj = self.object_declare() 
        conn = obj.createCon()
        data = pd.read_sql_query('''SELECT * FROM BOOKBORROWED''', conn)
        data['borroweddate'] = pd.to_datetime(data.borroweddate).dt.date
        counts = data['borroweddate'].value_counts().sort_index()
        borrowed_counts_df = counts.rename_axis('borroweddate').reset_index(name='counts')
        returned_counts_df = pd.read_sql_query('''select returneddate, count(returneddate)
        from bookborrowed group by returneddate order by returneddate;''', conn)
        returned_counts_df = returned_counts_df[returned_counts_df['returneddate'].notnull()]

        fig = plt.figure()
        axis1 = fig.add_subplot(211)
        borrowed_counts_df.plot(ax=axis1, color=['black'])
        borrowed_counts_df.plot.bar(rot=0, ax=axis1, color=['red'])
        axis1.set_xticklabels(borrowed_counts_df['borroweddate'], fontsize=5)
        axis1.set_xlabel("Book borrow date")
        axis1.set_ylabel("Number of books borrowed")
        axis1.set_title("Number of books borrowed day-wise")
        axis1.get_legend().remove()

        axis2 = fig.add_subplot(212)
        returned_counts_df.plot(ax=axis2, color=['black'])
        returned_counts_df.plot.bar(rot=0, ax=axis2, color=['green'])
        axis2.set_xticklabels(returned_counts_df['returneddate'], fontsize=5)
        axis2.set_xlabel("Book return date")
        axis2.set_ylabel("Number of books returned")
        axis2.set_title("Number of books returned day-wise")
        axis2.get_legend().remove()

        fig.tight_layout()

        fig.savefig('static/day_wise.pdf')

        obj.closeCon(conn)

    def create_week_graph(self):

        obj = self.object_declare()
        conn = obj.createCon()
        data = pd.read_sql_query('''SELECT * FROM BOOKBORROWED''', conn)
        data['borroweddate'] = pd.to_datetime(data.borroweddate).dt.date
        data['week'] = pd.to_datetime(data.borroweddate).dt.week

        data['week_range'] = np.nan

        for i in range(0, len(data)):
            data['week_range'][i] = self.foo(datetime.now().year, int(data['week'][i]))

        borrowed_counts = data['week_range'].value_counts().sort_index()
        borrowed_counts_df = borrowed_counts.rename_axis('week range').reset_index(name='borrowed_counts')

        returned_df = data[data['returneddate'].notnull()]
        returned_counts = returned_df['week_range'].value_counts().sort_index()
        returned_counts_df = returned_counts.rename_axis('week range').reset_index(name='returned_counts')

        fig = plt.figure()
        axis1 = fig.add_subplot(211)
        borrowed_counts_df.plot(ax=axis1, color=['black'])
        borrowed_counts_df.plot.bar(rot=0, ax=axis1, color=['red'])
        axis1.set_xticklabels(borrowed_counts_df['week range'], fontsize=5)
        axis1.set_xlabel("Book borrow week")
        axis1.set_ylabel("Number of books borrowed")
        axis1.set_title("Number of books borrowed week-wise")
        axis1.get_legend().remove()

        axis2 = fig.add_subplot(212)
        returned_counts_df.plot(ax=axis2, color=['black'])
        returned_counts_df.plot.bar(rot=0, ax=axis2, color=['green'])
        axis2.set_xticklabels(returned_counts_df['week range'], fontsize=5)
        axis2.set_xlabel("Book return week")
        axis2.set_ylabel("Number of books returned")
        axis2.set_title("Number of books returned week-wise")
        axis2.get_legend().remove()

        fig.tight_layout()

        fig.savefig('static/week_wise.pdf')

        obj.closeCon(conn)

    def create_popularbook_graph(self):

        obj = self.object_declare()
        conn = obj.createCon()
        data = pd.read_sql_query('''select title,count(borroweddate), count(returneddate)
            from book, bookborrowed where book.bookid = bookborrowed.bookid
            group by title order by COUNT(borroweddate) DESC limit 3;''', conn)

        fig, ax = plt.subplots()
        graph3 = data.plot.barh(rot=90, ax=ax, color=['blue', 'maroon'])
        ax.set_yticklabels(data.title)
        ax.set_xlabel("Number of times borrowed/returned")
        ax.set_ylabel("Book name")
        ax.set_title("Three most popular books in the library")
        ax.legend(["borrowed", "returned"])
        plt.savefig("static/popularbooks.pdf")
