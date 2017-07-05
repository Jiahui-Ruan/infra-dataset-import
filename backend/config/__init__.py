from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from file_reader import FileReader

async_mode = 'eventlet'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, async_mode=async_mode)

state_dict = {
            'step': 1,
            'bagParamDict': {},
            'allBag': [],
            'selectBag': []
}
cmd_list = FileReader().get_all_cmd('config/steps.yaml')
