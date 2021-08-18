from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            flash('this email is alerady present ')
            return render_template('register.html')
        password = generate_password_hash(request.form['password'],method='pbkdf2:sha256',salt_length=8)
        users = User(
            name = request.form['name'],
            email = request.form['email'],
            password = password,
        )
        db.session.add(users)
        db.session.commit()
        login_user(users)
        return redirect(url_for('secrets',name = request.form['name']))
    return render_template("register.html",logged_in=current_user.is_authenticated)


@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        given_password = request.form['password']
        user = User.query.filter_by(email=request.form['email']).first()
        if user:
            if check_password_hash(user.password,given_password):
                login_user(user)
                return redirect(url_for('secrets',name = user.name))
            else:
                flash('you have entered a wrong password')
        else:
            flash('This email id is not present in our Data base')
            return render_template('login.html',logged_in=current_user.is_authenticated)
    return render_template("login.html",logged_in=current_user.is_authenticated)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/secrets')
@login_required
def secrets():
    name = request.args.get('name')
    return render_template("secrets.html",name = name,logged_in=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
def download():
    return send_from_directory('static','files/cheat_sheet.pdf')


if __name__ == "__main__":
    app.run(debug=True)
