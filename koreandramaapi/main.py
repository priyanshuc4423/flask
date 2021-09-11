from flask import Flask,request,render_template,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dramas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Form(FlaskForm):
    name = StringField(label = 'name', validators=[DataRequired()] )
    rating = IntegerField(label='rating',validators=[DataRequired()])
    description = StringField(label='description',validators=[DataRequired()])
    submit = SubmitField(label='submit')

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def get_data(self):
        dictonary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictonary


@app.route('/add',methods = ['GET','POST'])
def run():
    form = Form()
    if form.validate_on_submit():
        post = BlogPost(
            name = form.name.data,
            rating = form.rating.data,
            description = form.description.data
        )
        db.session.add(post)
        db.session.commit()
        return 'ADDED DATA'

    return render_template('add.html',form =form)
@app.route("/")
def show():
    data = BlogPost.query.all()
    datas = [ BlogPost.get_data(dat) for dat in data]
    return jsonify(datas)

@app.route('/select')
def select():
    id = request.args.get('id')
    data = BlogPost.query.get(id)
    if data == []:
        return jsonify(post={
            'ERROR':'ID INVALID'
        })
    else:
        return jsonify(BlogPost.get_data(data))

@app.route('/addblog',methods = ['POST'])
def addblog():
    data = BlogPost(
        name = request.args.get('name'),
        rating = request.args.get('rating'),
        description = request.args.get("description")
    )
    print(request.args.get('name'),request.args.get('rating'),request.args.get("description"))
    db.session.add(data)
    db.session.commit()
    return jsonify(added={
        'SUCC':'ADDITION WAS SUCCESEFULL'
    })


@app.route('/delete',methods = ['POST'])
def deleteblog():
    if 'yellow' == f"{request.args.get('lock')}":
        id = request.args.get('id')
        data = BlogPost.query.get(id)
        print(data)
        if data != []:
            db.session.delete(data)
            db.session.commit()
            return jsonify(deleted={
                'DELETED':"DATA DELETED"
            })
        else:
            return  jsonify(ERROR={
                'ERROR':'INVALID ID'
            })
    else:
        return jsonify(ERROR={
            'ERROR': 'INVALID ID'
        })


@app.route('/update-blog/<int:id>')
def update(id):
    id = id
    try:
        data = BlogPost.query.get(id)
        data.rating = request.args.get('rating')
        db.session.commit()
        return jsonify(UPDATED={
            'UPDATED':"DATA UPDATED"
        }

        )
    except:
        return jsonify(ERROR={
            'ERROR':"ERROR 404"
        })







@app.route("/rating")
def rating():
    rating = request.args.get('rating')
    datas = BlogPost.query.filter_by(rating = rating)
    data = [BlogPost.get_data(dat) for dat in datas]
    if data == []:
        return jsonify(data={
            'ERROR':"NO RATING FOUND"
        }

        )
    else:
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)