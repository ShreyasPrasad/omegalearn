#!/usr/bin/env python3

from docopt import docopt
from flask import Flask, flash, render_template, request, url_for, redirect
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from opentok import OpenTok
import os
import sys
from sqlalchemy.exc import ProgrammingError

from omegabase.omegabase import Omegabase
from util.connect_with_sqlalchemy import (build_sqla_connection_string,
                                          test_connection)
from util.exception_handling import render_error_page


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")


_URL = sys.argv[1]
_MAX_RECORDS = 20
print(_URL)

chrome_ids = {}

# if _URL is None:  # No --url flag; check for environment variable DB_URI
# environment_connection_string = os.environ.get('DB_URI')
# CONNECTION_STRING = build_sqla_connection_string(
#     environment_connection_string)
# else:  # url was passed with `--url`
CONNECTION_STRING = build_sqla_connection_string(_URL)
# Load environment variables from .env file

# Instantiate the movr object defined in movr/movr.py
omegabase = Omegabase(CONNECTION_STRING, max_records=_MAX_RECORDS)

# Verify connection to database is working.
# Suggest help if common errors are encountered.
test_connection(omegabase.engine)


def get_tok_session():
    session = opentok.create_session()
    return session.session_id


def remove_user(data):
    chrome_id = data["chrome_id"]
    url = data["url"]
    if chrome_id in chrome_ids:
        if url in chrome_ids[chrome_id]:
            chrome_ids[chrome_id].remove(url)

    active_users = omegabase.leave_call(url)

    leave_room(url)

    emit("leave call", {"url": url, "active_users": active_users}, room=url)

    return


def update_user(data):
    """Update the user's current active tab"""
    chrome_id = data["chrome_id"]
    url = data["url"]
    if chrome_id in chrome_ids:
        if url not in chrome_ids[chrome_id]:
            chrome_ids[chrome_id].add(url)
    else:
        chrome_ids[chrome_id] = set([url])

    # Check for number of active users on url
    active_users, session_id = omegabase.join_call(url)
    if not session_id:
        session_id = get_tok_session()
        omegabase.start_call(url, session_id)
    
    join_room(url)

    emit("session found", {"url": url, "active_users": active_users, "session_id": session_id}, room=url)  # broadcast=True)
    return


api_key = "47084444"
api_secret = "1846a2e0f1df2138b0c036f6448cc3b8747b5d6f"
opentok = OpenTok(api_key, api_secret)
#session = opentok.create_session()
#session_id = session.session_id


@app.route('/', methods=["GET", "POST"])
def landing():
    # token = opentok.generate_token(session_id)
    # , api_key=api_key, session_id=session_id, token=token)
    active_users = omegabase.join_call(url='learn.com')
    return render_template('session.html')


@app.route('/call/<session_id>', methods=["GET", "POST"])
def call(session_id):
    token = opentok.generate_token(session_id)
    omegabase.start_call(session_id)
    return render_template('index.html', api_key=api_key, session_id=session_id, token=token)


def messageReceived(methods=['GET', 'POST']):
    print('message received')


@socketio.on('start call')
def on_start_call(data, methods=['GET', 'POST']):
    if number_users(data["url"]) <= 1:
        emit("no other users", {})
    else:
        session = get_tok_session(data["url"])
        token = opentok.generate_token(session.session_id)
        omegabase.start_call(session_id)
        # broadcast=True)#, "static": url_for('static', filename='js/helloworld.js')}, broadcast=True)
        emit("call started", {"session_id": session.session_id,
                              "api_key": api_key, "token": token}, room=data["url"])


@socketio.on('url added')
def handle_url_added(data, methods=['GET', 'POST']):
    update_user(data)


@socketio.on('url removed')
def handle_url_removed(data, methods=['GET', 'POST']):
    remove_user(data)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
