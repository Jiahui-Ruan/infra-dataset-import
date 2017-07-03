from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

async_mode = 'eventlet'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, async_mode=async_mode)
state_dict = {}
