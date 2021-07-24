
from flask import Flask
from random import randint

app = Flask(__name__)
real_number = randint(1,9)
print(real_number)
@app.route("/")
def homepage():
    return "<h1>guess the number from 0 to 9</h1>"\
    "<br><img src= 'https://media.giphy.com/media/24pBw18bgHMPu/giphy.gif'>"



@app.route("/<int:number>")
def guessnumber(number):
    if real_number == number:
        return "<h1> You have found me <h1>" \
                "<img src = 'https://media.giphy.com/media/d3HeU0IDO2jLy/giphy.gif'>"
    elif real_number < number:
        return "<h1> Too high <h1>" \
                "<img src = 'https://media.giphy.com/media/3o6Zt4FtlVT31FzlFC/giphy.gif'>"
    elif real_number > number:
        return "<h1> Too low <h1>" \
                "<img src = 'https://media.giphy.com/media/J4yM4i6OgymtYBlpFj/giphy.gif'>"





if __name__ == '__main__':
    app.run(debug=True)
