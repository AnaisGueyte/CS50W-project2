import os

from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "Imagine a world without StackOverflow"
socketio = SocketIO(app)


import routes

if __name__ == "__main__":
	app.run(routes, debug=True)


