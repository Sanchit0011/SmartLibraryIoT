from flask import Flask, render_template, request, Blueprint, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField
from psql import dbCon
from wtforms.validators import InputRequired, AnyOf
from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mischieveManaged'
bootstrap = Bootstrap(app)
# datepicker(app)

# Login page form


class LoginForm (FlaskForm):
    username = StringField(
        'username', validators=[
            InputRequired(
                message='input required!'), AnyOf(
                ['jaqen'])])
    password = PasswordField(
        'password', validators=[
            InputRequired(
                message='input required!'), AnyOf(
                ['hghar'])])
    remember = BooleanField('remember me')


# Newbook
class NewBook(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    try:
        publisheddate = DateField(
            'Published Date', validators=[
                InputRequired()], format='%Y-%m-%d')
    except BaseException:
        print("Enter the date dd-mm-yyyy format")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.username.data
            return redirect(url_for('addBook'))
    else:
        return render_template('index.html', form=form)


@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    form = NewBook()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        publisheddate = request.form.get('publisheddate')
        abook = (
            """ INSERT INTO book (bookid, title, author, publisheddate)
            VALUES (default, %s, %s, %s) """
        )
        dbCon().insUpDel(abook, title, author, publisheddate)
        return "Book added to the database"
    return render_template('addBook.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
