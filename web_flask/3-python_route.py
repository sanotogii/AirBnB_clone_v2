#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """
    hello hbnb function
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    hbnb route function
    """
    return 'HBNB'


@app.route('/python/<text>', strict_slashes=False)
@app.route('/c/<text>', strict_slashes=False)
def display(text):
    """
    Displays C followed by the value of text
    """
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port='5000')
