#!/usr/bin/python3
"""
script that starts a Flask web application
"""

from flask import Flask, render_template
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


@app.route('/c/<text>', strict_slashes=False)
def display(text):
    """
    Displays C followed by the value of text
    """
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def display_python(text='is_cool'):
    """
    Displays python followed by the value of text
    """
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def display_n(n: int) -> int:
    """
    Displays an integer number
    """
    return '{} is a number'.format(n)


@app.route('number_template/<int:n>', strict_slashes=False)
def display_html(n: int) -> int:
    """
    Displays an integer number
    """
    return render_template('5-number.html')


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port='5000')
