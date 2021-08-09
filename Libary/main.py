from flask import Flask, render_template, request, redirect, url_for
import flask_sqlalchemy
from typing import Callable
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = flask_sqlalchemy.SQLAlchemy(app)

@app.route('/')
def home():
    pass
    # # all_books = db.session.query(Book).all()
    # return render_template("index.html",list = all_books)


@app.route("/add",methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        pass
        # newbook = Book(name = request.form['name'],author = request.form['author'],rating = request.form['rating'])
        # db.session.add(newbook)
        # db.session.commit()


    return render_template("add.html")



if __name__ == "__main__":
    app.run(debug=True)

