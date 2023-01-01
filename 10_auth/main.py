from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
# Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods = ["GET","POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))


        secure_password = generate_password_hash(
                            password= request.form.get("password"), 
                            method = "pbkdf2:sha256", 
                            salt_length = 8
                            )

        new_user = User(
                email = request.form.get("email"),
                password = secure_password,
                name = request.form.get("name")
                )

        db.session.add(new_user)
        db.session.commit()


        login_user(new_user)
        flash('Logged in successfully.')

        return redirect(url_for("secrets"))

    return render_template("register.html")


@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":

        user_email = request.form.get("email")
        user_password = request.form.get("password")

        user = User.query.filter_by(email = user_email).first()


        if user:
            print(user)
            if check_password_hash(user.password, user_password):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for("secrets"))

            else:   
                flash('Wrong user name or password.')

            
        else: 
            flash('No Data for this E-mail address.')
            
        

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download/<filename>')
@login_required
def download(filename):

     return send_from_directory(
                            directory=app.static_folder, 
                            path=f'files/{filename}'
                            )
    # return {"Your": "MAMA"}


if __name__ == "__main__":
    app.run(debug=True)
