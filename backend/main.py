from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

@app.route('/', methods=["GET", "POST"])
def landing():
    return "Start Call"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost')

                         
