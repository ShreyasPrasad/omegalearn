from opentok import OpenTok

api_key = "47084444"
api_secret = "1846a2e0f1df2138b0c036f6448cc3b8747b5d6f"


def CreateSession(_api_key, _api_secret):
    opentok = OpenTok(_api_key, _api_secret)
    session = opentok.create_session()
    return session.session_id

def StartSession(_api_key, session_id):
    token = opentok.generate_token(session_id)
    return render_template('index.html', api_key=_api_key, session_id=session_id, token=token)