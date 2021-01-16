from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO
#from vonage import api_key, api_secret, CreateSession, StartSession
from opentok import OpenTok

import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

api_key = "47084444"
api_secret = "1846a2e0f1df2138b0c036f6448cc3b8747b5d6f"
opentok = OpenTok(api_key, api_secret)
session = opentok.create_session()
session_id = session.session_id

@app.route('/', methods=["GET", "POST"])
def landing():
    token = opentok.generate_token(session_id)
    return render_template('index.html', api_key=api_key, session_id=session_id, token=token)

    #return "Start Call"

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost')

                         
