from flask import Flask, render_template, request
import datetime as dt

app = Flask(__name__)




@app.route("/")
def index():
    return render_template('index.html', year = dt.datetime.now().year)


@app.route("/login", methods=["POST"])
def receive_data():
    name = request.form["username"]
    password = request.form["password"]
    return f"<h1>{name}, {password}</h1>"

if __name__=='__main__':
    app.run(debug=True)

