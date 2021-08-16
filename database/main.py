from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import SelectField
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


coffes_strength = ['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕']
wifi_strength = ['🌐','🌐🌐','🌐🌐🌐','🌐🌐🌐🌐','🌐🌐🌐🌐🌐']
power_strength = ['⚡','⚡⚡','⚡⚡⚡','⚡⚡⚡⚡','⚡⚡⚡⚡⚡']

class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Location URL',validators=[DataRequired()])
    opentime = StringField(label='Open Time', validators=[DataRequired()])
    closingtime = StringField(label='closingtime',validators=[DataRequired()])
    coffe = SelectField(label='coffe taste',choices =[(caffe,caffe) for caffe in coffes_strength],validators=[DataRequired()] )
    wifi = SelectField(label="WIFI",choices=[(strength,strength) for strength in wifi_strength],validators=[DataRequired()])
    power = SelectField(label='POWER',choices=[(powers) for powers in power_strength],validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods = ['POST','GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv','a',encoding="utf-8",newline="") as file:
            writer = csv.writer(file)
            writer.writerow([form.cafe.data,form.location.data,form.opentime.data,form.closingtime.data,form.coffe.data,form.wifi.data,form.power.data])

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='',encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
