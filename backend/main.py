from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=["GET", "POST"])
def landing():
    return "Start Call"

if __name__ == '__main__':
    app.run(debug=True, host='localhost')

                         
