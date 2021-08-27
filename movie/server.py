from flask import url_for,request,render_template,redirect,abort,Flask,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import UserMixin,login_user,login_required,LoginManager,current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Info,Login
from functools import wraps
admin = ['priyanshuc4423@gmail.com','priyanshuc529@gmail.com']
app = Flask(__name__)
app.config['SECRET_KEY'] = 'allyouwannadoiscocohangingoutwithyouisnogo'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movie.db'
Bootstrap(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, unique=True, nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(500), unique=True, nullable=False)
    video = db.Column(db.String(500), nullable=True)

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(500),nullable = False)
    email = db.Column(db.String(500),unique = True,nullable = False)
    password = db.Column(db.String(500),nullable = False)

@login_manager.user_loader
def load_user(data_id):
    return User.query.get(int(data_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('main.html')

def admin_perm(f):
    @wraps(f)
    def decorate(*args,**kwargs):
        if current_user.email in admin and current_user.is_authenticated:
            return f(*args,**kwargs)
        else:
            abort(status=403,description = 'YOU DONT HAVE ACCESS')
    return decorate





@app.route('/register',methods =['GET','POST'])
def register():
    form = Info()
    if form.validate_on_submit():
        if form.password.data == form.repassword.data:
            email = form.email.data
            user = User.query.filter_by(email = email).first()
            if user:
                flash('THIS EMAIL ALEARDY EXIST')
                return render_template('login.html',form = form)
            password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            data = User(name = form.name.data,email = form.email.data,password = password)
            db.session.add(data)
            db.session.commit()
            login_user(data)
            return redirect(url_for('get_data'))


        else:
            flash('THE PASSWORD DOSENT MATCH')
            return render_template('login.html',form =form)


    return render_template('login.html',form = form)



@app.route('/movies',methods = ['GET','POST'])
@login_required
def get_data():
    page = request.args.get('page',1,type=int)
    form = Data.query.paginate(page=page,max_per_page=10)

    return render_template('index.html',form = form,current_user = current_user,admin =admin)




@app.route("/search",methods = ['GET','POST'])
def search():
    print(request.method)
    if request.method == 'POST':
        name = ''
        names = request.form['search'].capitalize().split(' ')
        if len(names) > 1:
            for na in names:
                name += f"{na.capitalize()} "
        else:
            name += names[0].capitalize()

        get_data = Data.query.filter_by(name=name.strip()).first()

        if get_data:
            datagiven = True
            return render_template('search.html',data = get_data,datagiven = datagiven,current_user =current_user)
        else:
            datagiven = False
            return render_template('search.html',data = get_data,datagiven = datagiven,current_user =current_user)

        # some_name = ''
        # names = request.form['search'].split(" ")
        # print(names[0].capitalize(),names)
        # if len(names) > 1:
        #     for new_name in names:
        #         some_name += f"{new_name.capitalize()} "
        #     else:
        #         some_name += f"{names[0].capitalize()}"
        # print(some_name)
        # get_data = Data.query.filter_by(name=some_name.strip()).first()
        # print(get_data)

@app.route('/delete')
@admin_perm
def delete():
    name = request.args.get('name')
    data = Data.query.filter_by(name=name).first()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('get_data'))

@app.route('/login',methods = ['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        data = User.query.filter_by(email=form.email.data).first()
        if data:
            if check_password_hash(data.password,form.password.data):
                login_user(data)
                return redirect(url_for('get_data'))
            else:
                flash('INVALID PASSWORD','error')
                return render_template('register.html',form = form)
        else:
            flash('THE USER ID DOESNT EXIST','error')
            return render_template('register.html',form = form)
    return render_template('register.html',form = form)



if __name__ == "__main__":
    app.run(debug=True)

