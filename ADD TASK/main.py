from flask import Flask,request,render_template,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap




app = Flask(__name__)
app.config["SECRET_KEY"] = 'sjosnlvdnovheoik'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)

class Form(FlaskForm):
    name = StringField(label='name',validators=[DataRequired()])
    piority = SelectField(label='piority',choices=['HIGH','MEDIUM','LOW'],validators=[DataRequired()])
    description = StringField(label = 'Description',validators=[DataRequired()])
    submit = SubmitField(label='submit')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    piority = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
db.create_all()



@app.route("/")
def table():
    form = Task.query.all()

    return render_template('table.html',form = form)



@app.route('/add', methods = ['GET','POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        new_task = Task(
            name=form.name.data,
            piority=form.piority.data,
            description=form.description.data

        )
        print(form.piority.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('table'))
    return  render_template('index.html',form = form)

@app.route("/delete/<int:id>")
def delete(id):
    get_task = Task.query.get(id)
    db.session.delete(get_task)
    db.session.commit()
    return redirect(url_for('table'))

@app.route("/update/<int:id>",methods = ['GET','POST'])
def update(id):
    data = Task.query.get(id)
    form = Form(
        name = data.name,
        description = data.description,
        piority = data.piority,
    )
    if form.validate_on_submit():
        data.name = form.name.data
        data.description = form.description.data
        data.piority = form.piority.data
        db.session.commit()
        return redirect(url_for('table'))
    return render_template('index.html',form = form)


if __name__ == '__main__':
    app.run(debug=True)