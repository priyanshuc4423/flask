from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length
import email_validator
from flask_bootstrap import Bootstrap
class Forms(FlaskForm):
    name = StringField(label="name",validators=[DataRequired()])
    email = StringField(label="email",validators=[Email(message='please enter valid email id ',granular_message=True,check_deliverability=True),DataRequired()])
    password = PasswordField(label="password",validators=[DataRequired(),Length(min=8,message='your password should be 8 words long')])
    submit = SubmitField(label="login")

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "SOMETHING COMPLICATED AFF"

@app.route("/login",methods = ['GET','POST'])
def home():
    a = Forms()
    if a.validate_on_submit():
        print(a.password.data)
        if a.email.data == "admin@email.com"and a.password.data == "12345678":
            return render_template('success.html',new_form = a)
        else:
            return render_template('denied.html')

    return render_template('index.html',new_form = a)



@app.route("/")
def login():
    return render_template("login.html")





if __name__ == '__main__':
    app.run(debug=True)