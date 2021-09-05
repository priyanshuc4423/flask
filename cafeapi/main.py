from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_get(self):
        dictonary = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return dictonary




@app.route("/")
def home():
    return render_template("index.html")




    

## HTTP GET - Read Record
@app.route('/random')
def rand():
    cafes = Cafe.query.all()
    random_cafe = random.choice(cafes)
    return jsonify(Cafe.to_get(random_cafe))


@app.route("/all")
def all():
    cafes = Cafe.query.all()
    cafe = [Cafe.to_get(data) for data in cafes]
    return jsonify(cafe)

@app.route('/search')
def search():
    location = request.args.get('loc')

    cafes = Cafe.query.filter_by(location =f'{location}')
    cafe = [ Cafe.to_get(caf) for caf in cafes]
    if cafe != []:
        return jsonify(cafe)
    else:

        return jsonify(cafe = {
            'error':"location not found"
        })


## HTTP POST - Create Record
@app.route("/add",methods = ['POST'])
def add():
    cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )

    return jsonify(cafe={
        'result':"the cafe was added successfully"
    })


## HTTP PUT/PATCH - Update Record

@app.route('/upadate/<int:id>',methods = ['POST'])
def update(id):
    id = id
    try:
        cafe = Cafe.query.get(id)
        cafe.coffee_price = request.args.get('coffee_price')
        db.session.commit()
        return jsonify(cafe ={
            'UPDATED':"THE PRICE IS UPDATED"
        })
    except:
        return jsonify(cafe={
            'OH NO': "ERROR 404 HUMAN NOT FOUND"
        })


@app.route("/delete/<int:id>",methods = ['POST'])
def delete(id):
    if 'key' == request.args.get('api_key'):
        cafe = Cafe.query.get(id)
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(cafe={
            'DELETE':"RECORD WAS DELETE"
        })
    else:
        return jsonify(cafe={
            "ERROR":"YOU DONT HAVE ACCESS TO THIS PORTAL"
        })








## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
