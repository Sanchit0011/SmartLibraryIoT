from flask import Flask, render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField
from psql import dbCon
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from wtforms.fields.html5 import DateField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecretkey!'
bootstrap = Bootstrap(app)
# datepicker(app)


class NewBook(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    try:
        publisheddate = DateField('Published Date', validators=[InputRequired()], format='%Y-%m-%d')
    except:
        print("Enter the date dd-mm-yyyy format")

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    form = NewBook()
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        publisheddate = request.form.get('publisheddate')
        abook=(
            """ INSERT INTO book (bookid, title, author, publisheddate)
            VALUES (default, %s, %s, %s) """
            )
        dbCon().insUpDel(abook, title, author, publisheddate)
        return "Book added to the database"
    return render_template('addBook.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
