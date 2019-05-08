from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, DateField 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecretkey!'

class NewBook(FlaskForm):
    booktitle = StringField('Title')
    author = StringField('Author')
    publisheddate = DateField('Published Date')
    

@app.route('/addBook', methods=['GET', 'POST'])
def addBook():
    addBook = NewBook()
    if addBook.validate_on_submit():
        return '<h1>The book {} has been added to the database.</h1>'.format(addBook.booktitle.data)
    return render_template('addBook.html', form=addBook)

if __name__ == "__main__":
    app.run(debug=True)
