from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, Optional, NumberRange
import requests


API_KEY = "fab68cdc1c880cf7f3ed4792a5e4b7df"
URL = "https://api.themoviedb.org/3"


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.app_context().push()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top10-movie-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), unique=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable = True)
    img_url = db.Column(db.String(250))

def upload_movie(title:str, year : int, description : str, rating : float, ranking : int, review : str, img_url : str):
    new_movie = Movie(title = title, year = year, description = description, rating = rating, ranking = ranking, review = review, img_url = img_url)
    db.session.add(new_movie)
    db.session.commit()

# Lesen Sie alle Benutzer aus der Datenbank
def get_all_movies():
    return Movie.query.all()


db.create_all()

# upload_movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

class Edit_Form(FlaskForm):
    new_rating = FloatField("Your Rating out of 10", validators = [DataRequired(), NumberRange(0, 10)])
    new_review = StringField("Your Review", validators = [Optional()])
    btn_submit = SubmitField("Done")


class Add_Form(FlaskForm):
    movie_title = StringField("Movie Title", validators = [DataRequired()])
    btn_submit = SubmitField("Add Movie")
    


@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()


    return render_template("index.html", movies = all_movies)



@app.route("/edit", methods = ["GET", "POST"])
def edit():
    form =  Edit_Form()
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)

    if form.validate_on_submit():
        movie.rating = float(form.new_rating.data)
        movie.review = form.new_review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie = movie, form = form)



@app.route("/delete")
def delete_movie():   
    movie_id = request.args.get("id")
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for('home'))



@app.route("/add", methods = ["GET", "POST"])
def add_movie():
    form = Add_Form()
    if form.validate_on_submit():
        params = {
        "api_key" : API_KEY,
        "query" : form.movie_title.data
        }
        data = requests.get(url=f"{URL}/search/movie", params=params)
        return render_template("select.html", movie_titles = data)

    return render_template("add.html", form = form)



@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    params = {
    "api_key" : API_KEY,
    }
    data = requests.get(url=f"{URL}/movie/{movie_id}", params=params)
    movie = data.json()
    # upload_movie(title = movie["title"],
    #             year = movie["release_date"][:4],
    #             description = movie["overview"],
    #             # rating = None,
    #             # ranking = None,
    #             # review = None,
    #             img_url = f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'),
    new_movie = Movie(title = movie["title"],
                year = movie["release_date"][:4],
                description = movie["overview"],
                # rating = None,
                # ranking = None,
                # review = None,
                img_url = f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}')
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for('edit', id=new_movie.id))

        

    
    


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
