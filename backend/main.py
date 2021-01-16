from flask import Flask, render_template, request, url_for, redirect
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from opentok import OpenTok
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# Replace with Cockroach
site_users = {}
users_current_site = {}
def add_user(url, user_id):
    def remove_user(user_id):
        try:
            site_users[users_current_site[user_id]].remove(user_id)
        except:
            return
    try:
        site_users[url].add(user_id)
    except KeyError:
        site_users[url] = set([user_id])
    finally:
        remove_user(user_id)
        users_current_site[user_id] = url

def number_users(url):
    return len(site_users[url])

def update_user(data):
    """Update the user's current active tab"""
    print(data)
    add_user(data["url"], data["user_id"])
    emit("nusers", number_users(data["url"]), broadcast=True)

api_key = "47084444"
api_secret = "1846a2e0f1df2138b0c036f6448cc3b8747b5d6f"
opentok = OpenTok(api_key, api_secret)
session = opentok.create_session()
session_id = session.session_id

@app.route('/', methods=["GET", "POST"])
def landing():
    token = opentok.generate_token(session_id)
    return render_template('index.html', api_key=api_key, session_id=session_id, token=token)
 
def messageReceived(methods=['GET', 'POST']):
    print('message received')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    emit('my response', json, callback=messageReceived)

#@socketio.on('connect')
#def handle_user_connect(json, methods=['GET', 'POST']):
#    update_user(json)

@socketio.on('start call')
def on_start_call(data, methods=['GET', 'POST']):
    if number_users(data[url]) <= 0:
        emit("no other users")
    else:
        # omegalearn stuff here
        emit("call started")

@socketio.on('page load')
def handle_page_load(data, methods=['GET', 'POST']):
    update_user(data)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='localhost')

                         
