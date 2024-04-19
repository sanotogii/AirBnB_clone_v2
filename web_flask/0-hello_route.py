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

	Returns:
		str: A greeting message.
	"""
	return "Hello HBNB!"

if __name__ == "__main__":
	"""
	For when the file is run directly.
	"""
	app.run(debug=True)
	app.run(host="0.0.0.0", port="5000")
