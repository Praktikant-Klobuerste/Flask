from flask import Flask, render_template, request
from flask_wtf import FlaskForm

app = Flask(__name__)

counter=0

#rendering the HTML page which has the button
@app.route('/')
def json():
    return render_template('json.html', counter=counter)


#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    global counter
    print ("Hello")
    counter +=1
    print(counter)
    return ("nothing")


if __name__ == '__main__':
    app.run(debug=True)
