from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class LibraryForm(FlaskForm):
    book_name = StringField("Book Name", validators=[DataRequired()])
    author = StringField("Book Author", validators=[DataRequired()])
    rating = SelectField("Rating", choices=[(i, i) for i in range(1, 11)] ,validators=[DataRequired()])
    btn_add = SubmitField("Add Book")

class EditForm(FlaskForm):
    new_rating = StringField("New Rating", validators=[DataRequired()])
    btn_submit = SubmitField("Change Rating")


##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


def upload_book(title, author, rating):
    new_book = Book(title=title, author=author, rating=rating)
    db.session.add(new_book)
    db.session.commit()


# Lesen Sie alle Benutzer aus der Datenbank
def get_all_books():
    return Book.query.all()


# Löschen Sie einen Benutzer aus der Datenbank
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()


def create_tables():
    db.create_all()



@app.route('/')
def home():
    return render_template("index.html", all_books = get_all_books())



@app.route("/add", methods = ["GET","POST"])
def add():
    form = LibraryForm()
    if form.validate_on_submit():
        upload_book(
            form.book_name.data,
            form.author.data,
            form.rating.data)

        print(Book.query.filter_by(title=form.book_name.data).first())

        return redirect(url_for('home'))


    return render_template("add.html", form = form)



@app.route("/edit", methods = ["GET", "POST"])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        book_id = request.args.get('id')
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = float(form.new_rating.data)
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit_rating.html", book=book_selected, form = form)




@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    delete_book(book_id)

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

