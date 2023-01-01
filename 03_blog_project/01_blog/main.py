from flask import Flask, render_template, url_for, redirect
import requests

BLOG_URL = "https://api.npoint.io/b91e8cb40f60a02fbb8f"

app = Flask(__name__)

@app.route('/')
def home():
    print("redirected")    
    return redirect(url_for("home_blog"))


@app.route('/blog')
def home_blog():
    blogs = requests.get(BLOG_URL).json()
    return render_template("index.html", blogs = blogs)


@app.route('/post/<id>')
def blog_post(id):
    blogs = requests.get(BLOG_URL).json()
    return render_template("post.html", blogs = blogs, id = int(id)-1)


if __name__ == "__main__":
    app.run(debug=True)
