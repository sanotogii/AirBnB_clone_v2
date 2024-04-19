#!/usr/bin/python3
"""
Implementing a Flask app
"""

from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """
    The home function decorated by / and unstrict slashes.
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Defines the route for hbnb """
    return "HBNB"


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port="5000")
