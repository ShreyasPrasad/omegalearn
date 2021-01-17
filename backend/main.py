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
users_current_site = {}
tok_sessions = {}

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


def get_tok_session(url):
    try:
        return tok_sessions[url]
    except KeyError:
        session = opentok.create_session()
        tok_sessions[url] = session
        return session


def remove_user(data):
    # Returns None if not found
    old_url = data["url"]
    if(old_url):
        # Update the room for the URL that the user was previously in
        #room = users_current_site[user_id]
        leave_room(old_url)
        chrome_ids[old_url].remove(data["chrome_id"])
        emit("nusers", number_users(old_url), room=old_url)
    else:
        return


def add_user(url, user_id):
    session = ""
    try:
        chrome_ids[url].add(user_id)
    except KeyError:
        chrome_ids[url] = set([user_id])
        session = get_tok_session(url)
    finally:
        users_current_site[user_id] = url
        if(len(chrome_ids[url] > 1)):
            emit("session found", {"session_id": session.session_id}, room=url)


def number_users(url):
    return len(chrome_ids[url])


def update_user(data):
    """Update the user's current active tab"""
    print(data)
    add_user(data["url"], data["chrome_id"])
    # Only address users for a particular URL
    room = data["url"]
    join_room(room)
    emit("nusers", number_users(data["url"]), room=room)  # broadcast=True)


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
    return render_template('index.html', api_key=api_key, session_id=session_id, token=token)


def messageReceived(methods=['GET', 'POST']):
    print('message received')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    emit('my response', json, callback=messageReceived)


@socketio.on('start call')
def on_start_call(data, methods=['GET', 'POST']):
    if number_users(data["url"]) <= 1:
        emit("no other users", {})
    else:
        session = get_tok_session(data["url"])
        token = opentok.generate_token(session.session_id)
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
