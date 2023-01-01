from flask import Flask, render_template, redirect, url_for
from post import Post
import requests



BLOG_URL = "https://api.npoint.io/b91e8cb40f60a02fbb8f"


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.app_context().push()


post_list = []
blog_raw_data = requests.get(url=BLOG_URL)

if blog_raw_data.status_code == 200: 
    blog = blog_raw_data.json()

    for post in blog: 
        post_obj = Post(
                id = post.get("id"),
                title = post.get("title"),
                subtitle = post.get("subtitle"),
                body = post.get("body"),
                img_url = post.get("img_url")
            )
        post_list.append(post_obj)

    print(post_list)

else:
    print(f"api status code = {blog_raw_data.status_code}")



@app.route("/")
def home():
    return render_template("index.html", blog = post_list)


@app.route("/about")
def about_me():
    return render_template("about.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route('/post/<int:id>')
def post_page(id):
    print(id)
    return render_template("post.html", blog = post_list)


if __name__ == '__main__':
    app.run(debug=True)
