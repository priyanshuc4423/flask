from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length,data_required,email_validator,length
import email_validator
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'MAMACITA'

class new_form(FlaskForm):
    name = StringField(label='Name',validators=[DataRequired()])
    email = StringField(label='Email',validators=[DataRequired(),Email(message="please write a valid email id")])
    password = PasswordField(label='Password',validators=[DataRequired(),Length(min=8,message='your password should be 8 digits long')])
    submit = SubmitField(label='Submit')



@app.route('/',methods = ["GET",'POST'])
def forms():
    form = new_form()
    return render_template("index.html",form = form)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
