from flask import Flask, render_template
import datetime as dt
import requests
app = Flask(__name__)

AGIFY_URL = "https://api.agify.io"
GENDERIZE = "https://api.genderize.io"





# print(response_age["age"])
# print(response_gender["gender"])


@app.route("/")
def index():
    return render_template('index.html', text = "Lümmel", year = dt.datetime.now().year)


@app.route("/guess/<name>")
def bot(name):

    params = {
    "name" : name 
}

    response_age = requests.get(url = AGIFY_URL, params=params).json()
    response_gender = requests.get(url = GENDERIZE, params=params).json()
    return render_template('guess.html', name= name, age = response_age["age"], gender = response_gender["gender"])






if __name__=='__main__':
    app.run(debug=True)