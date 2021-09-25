from flask import Flask,render_template,redirect,url_for,flash,request,abort
from flask_bootstrap import Bootstrap
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import Information



app = Flask(__name__)

app.config['SECRET_KEY'] = 'allyouwannadoiscocohangingoutwithyouisnogo'
bootstrap = Bootstrap(app)
@app.route('/',methods =['GET','POST'])
def trial():
    form = Information()
    if form.validate_on_submit():
        return ('YOU IN BOII')
    return render_template('index.html',form = form)

if __name__ == '__main__':
    app.run(debug=True)