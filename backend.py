from flask import Flask, render_template
from application_api import LibraryApi

app = Flask(__name__, static_folder='./resources')


@app.route('/')
def hello_world():
    return render_template('player.html')


@app.route('/library')
def library():
    l = LibraryApi()
    # l.add_new('/home/dhruv/Music/Music/new world order/Disturbed')
    # l.add_new('/home/dhruv/Music/Music/new world order/eminem/Eminem Collection/8 Mile Soundtrack')
    # l.add_new('/home/dhruv/Music/Music/Aisha (2010) ~ 320 VBR')
    return render_template('library.html')


def start_server():
    app.run()
