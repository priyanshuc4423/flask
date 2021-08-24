from flask import Flask,request,render_template,flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,Email
from flask_sqlalchemy import SQLAlchemy
from smtplib import SMTP
my_email = "jameswang8667@gmail.com"
my_password = "Jambajuice@713"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'allyouwannadoiscocohangingoutwithyouisnogo'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///forms.db'
Bootstrap(app)
db = SQLAlchemy(app)

class Info(FlaskForm):
    name = StringField(label='Name',validators=[DataRequired()],render_kw={'placeholder':'name'})
    phone = StringField(label="Phone",validators=[DataRequired()],render_kw={'placeholder':'phone'})
    Batch = SelectField(label='Batch',choices=['1st','2nd','3rd','4th'],validators=[DataRequired()],render_kw={'placeholder':'Batch'})
    Branch = SelectField(label='Branch',choices=['Visakhapatnam','Hyderabad','Bengaluru'],validators=[DataRequired()],render_kw={'placeholder':'Branch'})
    Pinnumber = StringField(label='Pin number',validators=[DataRequired()],render_kw={'placeholder':'pinnumber'})
    Department = SelectField(label='Department',choices=['Graphic Design','Content','Editor'],validators=[DataRequired()],render_kw={'placeholder':'Department'})
    email = StringField(label='Email',validators=[DataRequired(),Email(message='please enter a valid email id')])
    submit = SubmitField(label='Submit')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pinnumber = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(500),unique=True, nullable=False)
    Batch = db.Column(db.String(500), nullable=True)
    email = db.Column(db.String(250), nullable=True)
    branch = db.Column(db.String(250), nullable=True)
    department = db.Column(db.String(250), nullable=True)
db.create_all()


@app.route("/",methods = ['GET','POST'])
def home():
    form = Info()
    filled = False
    if form.validate_on_submit():
        if "@gitam.in" in form.email.data:
            name = form.name.data
            filled = True
            new_user = User(name = form.name.data,
                            phone = form.phone.data,
                            pinnumber = form.Pinnumber.data,
                            Batch =form.Batch.data,
                            branch = form.Branch.data,
                            department = form.Department.data)

            db.session.add(new_user)
            db.session.commit()
            with SMTP('smtp.gmail.com',587,timeout=180) as connection:
                connection.starttls()
                connection.login(user=my_email,password=my_password)
                info = f"Subject:INFO\n\nname{form.name.data}\nphone:{form.phone.data}\nbatch:{form.Batch.data}\nbranch:{form.Branch.data}\nemail:{form.email.data}\ndepartment:{form.Department.data}\ndepartment:{form.Pinnumber.data}"
                message = f"Subject:DONTREPLY APPLICATION RECIEVED\n\nThank you {name}\n we will get back to you as soon as possible till then enjoy our anime "
                connection.sendmail(from_addr=my_email,to_addrs="priyanshuc4423@gmail.com",msg=info)
                connection.sendmail(from_addr=my_email, to_addrs=f"{form.email.data}", msg=message)

            return render_template('index.html',name = name,filled = filled)
        else:
            flash("please enter a gitam maild in mail column")
            return render_template('index.html',filled = filled,form = form)


    return render_template('index.html',form = form,filled=filled)

@app.route('/video')
def video():
    return render_template('impossible.html')




if __name__ == "__main__":
    app.run(debug=True)

