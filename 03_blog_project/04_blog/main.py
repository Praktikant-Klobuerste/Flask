from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar

from forms import CreatePostForm, RegisterForm, LogInForm, CommentForm
from admin import admin_only

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.app_context().push()
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(250), nullable=True)
    date = db.Column(db.String(250), nullable=True)
    
    #This will act like a List of BlogPost objects attached to each User. 
    #The "author" refers to the author property in the BlogPost class.
    posts = relationship("BlogPost", back_populates="author")
    
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    #Create Foreign Key, "users.id" the users refers to the tablename of User.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="posts")
   
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    
db.create_all()



@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts)


@app.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():

        user = User.query.filter_by(email= form.email.data).first()
        print(user)
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:    
            new_user = User(
                name = form.name.data,
                email = form.email.data,
                password = generate_password_hash(form.password.data, salt_length=8),
                date = datetime.now().strftime("%B %d, %Y. %H:%M")
            )

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Successfully registerd")

            return redirect(url_for("get_all_posts"))

    return render_template("register.html", form = form)


@app.route('/login', methods = ["GET", "POST"])
def login():
    form = LogInForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email= email).first()

        if user:
            print(f"User found: {user.name}")
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for("get_all_posts"))
            else:
                flash("Wrong Password")

        else:
            flash(f"No user found with Email Address {email}")

        
    return render_template("login.html", form = form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged Out!")
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    return render_template("post.html", post=requested_post, form = form)
    


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post", methods = ["GET", "POST"])
@login_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=datetime.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods = ["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        # author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author.name = current_user.name
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
