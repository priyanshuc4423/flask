from wtforms import SubmitField,StringField,SelectField,PasswordField
from wtforms.validators import DataRequired,Email,Length
from flask_wtf import FlaskForm

class Info(FlaskForm):
    name = StringField(label='NAME',validators=[DataRequired()])
    email = StringField(label='EMAIL',validators=[DataRequired(),Email(message="ENTER A VALID EMAIL")])
    password = PasswordField(label='PASSWORD',validators=[DataRequired(),Length(min=8)])
    repassword = PasswordField(label='PASSWORD',validators=[DataRequired(),Length(min=8)])
    submit = SubmitField(label='Submit')

class Login(FlaskForm):
    email = StringField(label='email',validators=[DataRequired(),Email(message='ENTER A VALID MAIL')])
    password = PasswordField(label='password',validators=[DataRequired()])
    submit = SubmitField(label='Submit')