from getcontent import Getcontent

a = Getcontent()

def make_bold(function):
    def wrapper():
        return f'<b>{function()}</b>'
    return wrapper
def make_em(function):
    def wrapper():
        return f"<em>{function()}</em>"
    return wrapper

def make_underline(function):
    def wrapper():
        return f"<u>{function()}</u>"
    return wrapper


from flask import Flask
app = Flask(__name__)

@app.route('/')
@make_bold
@make_em
@make_underline
def hello_world():
    return 'Hello, World!'

@app.route('/movies')
def movie():
    content = a.newfunction()
    # for x in range(len(list)):
    return f'''<center><h1>{content[1].text}</h1>
                <br><img src = "https://media.giphy.com/media/Cn4OR6AI2SxY4/giphy.gif">
                <br><h1>{content[3].text}</h1>
                <br><img src = "https://media.giphy.com/media/3o7bufgPP70ra2ZVi8/giphy.gif">
                <br><h1>{content[5].text}</h1>
                <br><img src ="https://media.giphy.com/media/2C4h9RYRlcU5q/giphy.gif">
                <br><h1>{content[7].text}</h1>
                <br><img src = "https://media.giphy.com/media/TlrykTWuQMvmM/giphy.gif">
                <br><h1>{content[9].text}</h1>
                <br><img src = "https://media.giphy.com/media/l0IyooO1w2UxMZHuo/giphy.gif">
                <br><h1>{content[11].text}</h1>
                <br><img src = "https://media.giphy.com/media/PrGNf7O36heCs/giphy.gif"
                <br><h1>{content[13].text}</h1>
                <br><img src = "https://media.giphy.com/media/VfwIk1LD84CI/giphy.gif>"</center>'''\




if __name__ == '__main__':
    app.run(debug=True)
