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


def add_user(url, user_id):
    def remove_user(user_id):
        # Returns None if not found
        old_url = users_current_site.get(user_id)
        if(old_url):
            # Update the room for the URL that the user was previously in
            #room = users_current_site[user_id]
            leave_room(old_url)
            site_users[old_url].remove(user_id)
            emit("nusers", number_users(old_url), room=old_url)
        else:
            return
    remove_user(user_id)
    try:
        site_users[url].add(user_id)
    except KeyError:
        site_users[url] = set([user_id])
    finally:
        users_current_site[user_id] = url


def number_users(url):
    return len(site_users[url])


def update_user(data):
    """Update the user's current active tab"""
    print(data)
    add_user(data["url"], data["user_id"])
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
    url = omegabase.join_call(url='learn.com')
    return render_template('session.html')


@app.route('/call', methods=["GET", "POST"])
def call(session_id, token):
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
        emit("call started", {"session_id": session.session_id, "api_key": api_key,
                              "session_id": session.session_id, "token": token}, room=data["url"])


@socketio.on('page load')
def handle_page_load(data, methods=['GET', 'POST']):
    update_user(data)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
