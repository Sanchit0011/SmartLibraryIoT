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
    def UnameChk(form, field):
        if field.data != "jaqen":
            raise ValidationError("Invalid Login credentials !")

    def passChk(form, field):
        if field.data != "hghar":
            raise ValidationError("Invalid Login credentials !")

    username = StringField(
        'Username', validators=[
            InputRequired(), UnameChk])
    password = PasswordField(
        'Password', validators=[
            InputRequired(), passChk])


class ItemTable(Table):
    bookid = Col('bookid')
    title = Col('title')
    author = Col('author')
    publisheddate = Col('publisheddate')
    classes = ['table', 'table-hover', 'table-condensed']
    table_id = "sort"
    name = LinkCol('manage', 'delF', url_kwargs=dict(id='bookid'), attr='manage')


class NewBook(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    try:
        publisheddate = DateField('''Published Date
        ''', validators=[InputRequired()], format='%Y-%m-%d')
    except:
        print("Enter the date dd-mm-yyyy format")


@app.route('/', methods=['GET', 'POST'])
def index():
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
    q = ("""Select *
    from bookborrowed
    where bookid = %s """)
    rows = dbCon().selectQ(q, id)
    if len(rows) == 0:
        form = NewBook()
        table = ItemTable(items)
        dbCon().insUpDel("""DELETE FROM book WHERE book.bookid = %s """, id)
        return render_template('addBook.html', form=form, table=table, myModaldel="myModaldel")

    items = dbCon().selectQName("""select bookid,title,author,publisheddate,
        'delete' as manage from book""")
    books = dbCon().selectQ(""" Select status
        from bookborrowed inner join book
        on bookborrowed.bookid = book.bookid
        where bookborrowed.bookid = %s ORDER BY returneddate DESC LIMIT 1 """, id)
    if books[0][0] == "borrowed":
        form = NewBook()
        table = ItemTable(items)
        return render_template('addBook.html', form=form, table=table, myModalcantdel="myModalcantdel")
    elif books[0][0] == "returned":
        form = NewBook()
        table = ItemTable(items)
        dbCon().insUpDel("""DELETE FROM bookborrowed WHERE bookborrowed.bookid = %s """, id)
        dbCon().insUpDel("""DELETE FROM book WHERE book.bookid = %s """, id)
        return render_template('addBook.html', form=form, table=table, myModaldel="myModaldel")


@app.route("/vis")
def sendVis():
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


@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
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
    form = LoginForm()
    if "username" in session:
        session.pop("username")
        return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
