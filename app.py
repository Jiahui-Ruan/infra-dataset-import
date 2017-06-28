import webbrowser

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
    webbrowser.open('http://localhost:5005', autoraise=True)
    socketio.run(app, host='0.0.0.0', port=5005)
