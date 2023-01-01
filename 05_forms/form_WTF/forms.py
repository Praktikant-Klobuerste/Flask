from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length

# Create a new Flask app
app = Flask(__name__)

# Set a secret key for the app to use when signing cookies and other data
app.secret_key = "any-string-you-want-just-keep-it-secret"

# Enable CSRF protection for the form
app.config['WTF_CSRF_ENABLED'] = True


# Define the login form with email, password, and submit fields
# Each field has specified validators to ensure the data is valid
class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[
                                DataRequired(),
                                Email("This field requires a valid email address")])

    password = PasswordField(label='Password', validators=[
                                            DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')

    
# The index route renders the index.html template
@app.route("/")
def index():
    return render_template('index.html')


# The login route handles GET and POST requests for the login form
@app.route("/login", methods=["GET", "POST"])
def login():
    # Create a new login form
    login_form = LoginForm()

    # If the form was submitted using the POST method and the data is valid...
    if request.method == "POST" and login_form.validate_on_submit():
        # Do something with the data, such as logging in the user or saving the data to a database
        print(login_form.email.data )
        print(login_form.password.data)

    # Render the login.html template and pass the form object to the template
    return render_template('login.html', form=login_form)


# If the script is run directly, start the Flask development server
if __name__ == '__main__':
    app.run(debug=True)