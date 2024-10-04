from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Pagina de inicio</h1>'


@app.route('/Hello')
@app.route('/Hello/<name>')
@app.route('/Hello/<name>/<int:age>')
def Hello(name = None, age = None):
    if name == None and age == None:
        return "<h1>Hola Mundo</h1>"
    elif age == None:
        return f"<h1>Hola {name}"
    else:
        return f'Hola {name}, y tu edad es {age}'