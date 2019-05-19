from flask import Flask, render_template
from flask import request, send_file, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators, BooleanField, ValidationError
from psql import dbCon
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField
from flask_table import Table, Col, LinkCol
from visualisation import visual
import zipfile
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecretkey!'
bootstrap = Bootstrap(app)


class LoginForm (FlaskForm):
    """Match login creds with admin creds
    
    Arguments:
        FlaskForm {FlaskForm} -- Flask form to check fields and validations
    
    Raises:
        ValidationError: to check username
        ValidationError: to check password
    """
    def UnameChk(form, field):
        """username check
        
        Arguments:
            form {flask form} -- flask form submitted by user
            field {flask form field} -- field to check user input
        
        Raises:
            ValidationError: if username doesnt match
        """
        if field.data != "jaqen":
            raise ValidationError("Invalid Login credentials !")

    def passChk(form, field):
        """check password
        
        Arguments:
            form {flask form} -- flask form submitted by user
            field {flask form field} -- field to check user input
        
        Raises:
            ValidationError: if password incorrect
        """
        if field.data != "hghar":
            raise ValidationError("Invalid Login credentials !")

    username = StringField(
        'Username', validators=[
            InputRequired(), UnameChk])
    password = PasswordField(
        'Password', validators=[
            InputRequired(), passChk])


class ItemTable(Table):
    """create html table from dict and create delete button dynamically
    
    Arguments:
        Table {dictionary} -- row col values from query
    """
    bookid = Col('bookid')
    title = Col('title')
    author = Col('author')
    publisheddate = Col('publisheddate')
    classes = ['table', 'table-hover', 'table-condensed']
    table_id = "sort"
    name = LinkCol('manage', 'delF', url_kwargs=dict(id='bookid'), attr='manage')


class NewBook(FlaskForm):
    """validate title and author fields to be filled
    
    Arguments:
        FlaskForm {FlaskForm} -- form submitted by user
    """
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    try:
        publisheddate = DateField('''Published Date
        ''', validators=[InputRequired()], format='%Y-%m-%d')
    except:
        print("Enter the date dd-mm-yyyy format")


@app.after_request
def add_header(response):
    """add header in request toprevent browser for caching pages due to security reasons
    
    Arguments:
        response {http response} -- response going to browser
    
    Returns:
        http response -- with added no cache flag
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    """shows the login page if user is not logged in or has logged out
    
    Returns:
        login.html -- login page if invalid creds
        addbook url -- addBook url if login success
    """
    if 'username' not in session:
        form = LoginForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                session['username'] = 'admin'
                return redirect(url_for('addBook'))
            else:
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return redirect(url_for('addBook'))


@app.route('/item/<int:id>')
def delF(id):
    """delete book
    
    Arguments:
        id {int} -- book ID to delete
    
    Returns:
        login page -- if user try to do url manipulation without login
        addBook -- returns addBook page with appropriate info message
    """
    if 'username' in session:
        q = ("""Select *
        from bookborrowed
        where bookid = %s """)
        rows = dbCon().selectQ(q, id)
        books = dbCon().selectQ(""" Select status
            from bookborrowed inner join book
            on bookborrowed.bookid = book.bookid
            where bookborrowed.bookid = %s ORDER BY returneddate DESC LIMIT 1 """, id)
        if len(rows) == 0:
            dbCon().insUpDel("""DELETE FROM book WHERE book.bookid = %s """, id)
            items = dbCon().selectQName("""select bookid,title,author,publisheddate,
            'delete' as manage from book""")
            table = ItemTable(items)
            form = NewBook()
            return render_template('addBook.html', form=form, table=table, myModaldel="myModaldel")
        if books[0][0] == "borrowed":
            form = NewBook()
            items = dbCon().selectQName("""select bookid,title,author,publisheddate,
            'delete' as manage from book""")
            table = ItemTable(items)
            return render_template('addBook.html', form=form, table=table, myModalcantdel="myModalcantdel")
        elif books[0][0] == "returned":
            dbCon().insUpDel("""DELETE FROM bookborrowed WHERE bookborrowed.bookid = %s """, id)
            dbCon().insUpDel("""DELETE FROM book WHERE book.bookid = %s """, id)
            form = NewBook()
            items = dbCon().selectQName("""select bookid,title,author,publisheddate,
            'delete' as manage from book""")
            table = ItemTable(items)
            return render_template('addBook.html', form=form, table=table, myModaldel="myModaldel")
    else:
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route("/vis")
def sendVis():
    """Run alaytics and generate visualization from database
    
    Returns:
        file -- zip file containing graphs
    """
    if 'username' in session:
        if os.path.exists("Visual.zip"):
            os.remove("Visual.zip")
        if os.path.exists("static/day_wise.pdf"):
            os.remove("static/day_wise.pdf")
        if os.path.exists("static/week_wise.pdf"):
            os.remove("static/week_wise.pdf")
        if os.path.exists("static/popularbooks.pdf"):
            os.remove("static/popularbooks.pdf")
        vis = visual()
        vis.create_day_graph()
        vis.create_week_graph()
        vis.create_popularbook_graph()
        zipfile.ZipFile('Visual.zip', mode='w').write("static/day_wise.pdf")
        zipfile.ZipFile('Visual.zip', mode='a').write("static/week_wise.pdf")
        zipfile.ZipFile('Visual.zip', mode='a').write("static/popularbooks.pdf")
        return send_file("Visual.zip", as_attachment=True)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    """add book to database with name author and publush date
    
    Returns:
        template -- addBook page template with appropriate error message
    """
    if 'username' in session:
        form = NewBook()
        items = dbCon().selectQName("""select bookid,title,author,publisheddate,
        'delete' as manage from book""")
        table = ItemTable(items)
        if request.method == 'POST':
            title = request.form.get('title')
            author = request.form.get('author')
            publisheddate = request.form.get('publisheddate')
            abook = (
                """ INSERT INTO book (bookid, title, author, publisheddate)
                VALUES (default, %s, %s, %s) """
                )
            dbCon().insUpDel(abook, title, author, publisheddate)
            items = dbCon().selectQName("""select bookid,title,author,publisheddate,
            'delete' as manage from book""")
            table = ItemTable(items)
            return render_template('addBook.html', form=form, table=table, myModaladd="myModaladd")
        return render_template('addBook.html', form=form, table=table)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route('/logout')
def logMeOut():
    """logout admin from app to login page
    
    Returns:
        html -- login page
    """
    form = LoginForm()
    if 'username' in session:
        session['username'] = 'logout'
        session.pop('username',None)
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
