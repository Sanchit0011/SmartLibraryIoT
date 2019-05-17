# Imported the necessary modules
import pandas as pd
from psql import dbCon as psql
import numpy as np
from datetime import *
import warnings
import matplotlib as matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Defined the visual class
class visual():
    """The visual class is used to generate visualisations for book borrow 
    and return statistics. There are three visualisations generated:
    
    1. The first visualisation consists of two vertical bar graphs
    which depict the number of books being borrowed and returned per day.
    
    2. The second visualisation consists of two vertical bar graphs
    which depict the number of books being borrowed and returned per week.
    3. The third visualisation is a horizontal bar graph which depicts the 
    three most popular books in the library."""

    # Suppress all warnings
    warnings.simplefilter(action='ignore')
   
    # Function to create psql object
    def object_declare(self):
        """This function creates an object of the psql class and then return it.
        
        Returns:
            connection -- Object of the psql class.
        """
        obj = psql()
        return obj

    # Function to come up with week range
    def calc_week_range(self, year, week):
        """This function comes up with the week range based on a week number and a year. 
        First, the first date of the year is stored in a variable. Then, the number of days 
        are calculated based on the week number. The number of days and six plus the number of
        days are then seperately added to the variable to come up with the week range.
         
        Arguments:
            year {int} -- The year of the week range.
            week {int} -- The week which is used to come up with the week range.
        
        Returns:
            string -- The week range based on week number and year. 
        """
        
        # Calculates and returns week range based on week number and year
        firstdate = date(year,1,1)
        rangedate = timedelta(days = (week-1)*7)
        return str(firstdate + rangedate) + " " + "-" + " " + str(firstdate + rangedate + timedelta(days=6))
    
    # Function to create day-wise borrow and return visualisation
    def create_day_graph(self):
        """This function creates two vertical bar graphs with trend lines as subplots and combines them 
        into one main plot. The first bar graph depicts the number of books borrowed from the library 
        day-wise and the second one depicts the number of books being returned to the library day-wise."""

        # Creates psql object and creates connection to cloud db
        obj = self.object_declare() 
        conn = obj.createCon()
        
        # Retrieves bookborrowed date from cloud db
        data = pd.read_sql_query('''SELECT * FROM BOOKBORROWED''', conn)
        data['borroweddate'] = pd.to_datetime(data.borroweddate).dt.date
        
        # Gets number of books being borrowed day-wise and converts to dataframe  
        counts = data['borroweddate'].value_counts().sort_index()
        borrowed_counts_df = counts.rename_axis('borroweddate').reset_index(name='counts')
        
        # Gets number of books being returned day-wise and converts to dataframe 
        returned_counts_df = pd.read_sql_query('''select returneddate, count(returneddate) from
        bookborrowed group by returneddate order by returneddate;''', conn)
        returned_counts_df = returned_counts_df[returned_counts_df['returneddate'].notnull()]

        # Creates main plot
        fig = plt.figure()
        
        # Creates first subplot
        axis1 = fig.add_subplot(211)
        
        # Creates vertical bar graph depicting number of books borrowed day-wise
        borrowed_counts_df.plot(ax=axis1, color=['black'])
        borrowed_counts_df.plot.bar(rot=0, ax=axis1, color=['red'])
        axis1.set_xticklabels(borrowed_counts_df['borroweddate'], fontsize=5)
        axis1.set_xlabel("Book borrow date")
        axis1.set_ylabel("Number of books borrowed")
        axis1.set_title("Number of books borrowed day-wise")
        axis1.get_legend().remove()
        
        # Creates second subplot
        axis2 = fig.add_subplot(212)

        # Creates vertical bar graph depicting number of books returned day-wise
        returned_counts_df.plot(ax=axis2, color=['black'])
        returned_counts_df.plot.bar(rot=0, ax=axis2, color=['green'])
        axis2.set_xticklabels(returned_counts_df['returneddate'], fontsize=5)
        axis2.set_xlabel("Book return date")
        axis2.set_ylabel("Number of books returned")
        axis2.set_title("Number of books returned day-wise")
        axis2.get_legend().remove()
        
        fig.tight_layout()
        
        # Generates pdf containing both vertical bar graphs as a single plot
        fig.savefig('static/day_wise.pdf')
        
        # Close the cloud db connection
        obj.closeCon(conn)

    
    # Function to create week-wise borrow and return visualisation
    def create_week_graph(self):
        """This function creates two vertical bar graphs with trend lines as subplots and combines them 
        into one main plot. The first bar graph depicts the number of books borrowed from the library 
        week-wise and the second one depicts the number of books being returned to the library week-wise."""
        
        # Creates psql object and creates connection to cloud db
        obj = self.object_declare()
        conn = obj.createCon()
        
        # Retrieves bookborrowed date from cloud db
        data = pd.read_sql_query('''SELECT * FROM BOOKBORROWED''', conn)

        # Divides data dataframe into two based on borrowed date and returned date
        borrowed_data = data.loc[:, data.columns != 'returneddate']
        returned_data = data.loc[:, data.columns != 'borroweddate']
        returned_data = returned_data[returned_data['returneddate'].notnull()]

        returned_data = returned_data.reset_index(drop=True)

        borrowed_data['borroweddate'] = pd.to_datetime(borrowed_data.borroweddate).dt.date
        returned_data['returneddate'] = pd.to_datetime(returned_data.returneddate).dt.date
        
        # Creates week column for both borrowed_data and returned_data dataframes
        borrowed_data['week_borrowed'] = pd.to_datetime(borrowed_data.borroweddate).dt.week
        returned_data['week_returned'] = pd.to_datetime(returned_data.returneddate).dt.week
        
        # Creates week_range column for both borrowed_data and returned_data dataframes
        borrowed_data['week_range_borrowed'] = np.nan
        returned_data['week_range_returned'] = np.nan

        # Goes through length of borrowed_data df and calculates week range for each borrow week
        for i in range(0, len(borrowed_data)):
            borrowed_data['week_range_borrowed'][i] = self.calc_week_range(datetime.now().year, int(borrowed_data['week_borrowed'][i]))
           
        # Goes through length of returned_data df and calculates week range for each return week
        for i in range(0, len(returned_data)):   
            returned_data['week_range_returned'][i] = self.calc_week_range(datetime.now().year, int(returned_data['week_returned'][i]))
        
        # Gets number of books being borrowed week-wise and converts to dataframe  
        borrowed_counts = borrowed_data['week_range_borrowed'].value_counts().sort_index()
        borrowed_counts_df = borrowed_counts.rename_axis('week range').reset_index(name='borrowed_counts')
    
        # Gets number of books being returned week-wise and converts to dataframe
        returned_counts = returned_data['week_range_returned'].value_counts().sort_index()
        returned_counts_df = returned_counts.rename_axis('week range').reset_index(name='returned_counts')
        
        # Creates vertical bar graph depicting number of books borrowed week-wise
        fig = plt.figure()
        axis1 = fig.add_subplot(211)
        borrowed_counts_df.plot(ax=axis1, color=['black'])
        borrowed_counts_df.plot.bar(rot=0, ax=axis1, color=['red'])
        axis1.set_xticklabels(borrowed_counts_df['week range'], fontsize=5)
        axis1.set_xlabel("Book borrow week")
        axis1.set_ylabel("Number of books borrowed")
        axis1.set_title("Number of books borrowed week-wise")
        axis1.get_legend().remove()
      
        # Creates vertical bar graph depicting number of books returned week-wise
        axis2 = fig.add_subplot(212)
        returned_counts_df.plot(ax=axis2, color=['black'])
        returned_counts_df.plot.bar(rot=0, ax=axis2, color=['green'])
        axis2.set_xticklabels(returned_counts_df['week range'], fontsize=5)
        axis2.set_xlabel("Book return week")
        axis2.set_ylabel("Number of books returned")
        axis2.set_title("Number of books returned week-wise")
        axis2.get_legend().remove()

        fig.tight_layout()

        # Generates pdf containing both vertical bar graphs as a single plot
        fig.savefig('static/week_wise.pdf')
        
        # Close the cloud db connection
        obj.closeCon(conn)

    # Function to create visualisation depicting three most popular books 
    def create_popularbook_graph(self):
        """This function creates a horizontal grouped bar graph which depicts the  
        three most popular books based on the number of times it has been borrowed. 
        The number of borrows and returns for each of the three books are depicted as
        horizontal stacked bars."""

        # Creates psql object and creates connection to cloud db
        obj = self.object_declare()
        conn = obj.createCon()

        # Retrieves data for three most popular books in library
        data = pd.read_sql_query('''select title,count(borroweddate), count(returneddate) 
                                    from book, bookborrowed where book.bookid = bookborrowed.bookid 
                                    group by title order by COUNT(borroweddate) DESC limit 3;''', conn)
        
        # Creates horizontal grouped bar graph depicting three most popular books
        fig, ax = plt.subplots()
        graph3 = data.plot.barh(rot=90, ax=ax, color=['blue','maroon'])
        ax.set_yticklabels(data.title)
        ax.set_xlabel("Number of times borrowed/returned")
        ax.set_ylabel("Book name")
        ax.set_title("Three most popular books in the library")
        ax.legend(["borrowed", "returned"])
        
        # Generates pdf containing the horizontal grouped bar graph
        plt.savefig("static/popularbooks.pdf")

        # Close the cloud db connection
        obj.closeCon(conn)


# Creates visual class object and calls all functions
vis = visual()
vis.create_day_graph()
vis.create_week_graph()
vis.create_popularbook_graph()
