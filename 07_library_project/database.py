from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
# create the app
app = Flask(__name__)
app.app_context().push()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
         return(f"{self.title} - {self.author} - {self.rating}/10 ")
        

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

# create tables if they don't exist yet
create_tables()

# upload a book
# upload_book("Make it Stick", "Henry L. Roediger III und Mark A. McDaniel", 9.7)


# book_to_update = Book.query.filter_by(title="Harry Potter and the Chamber of Secrets").first()
# print(book_to_update)
print(Book.query.get(1))
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
db.session.commit()