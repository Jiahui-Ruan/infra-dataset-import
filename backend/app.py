import webbrowser
from config import app, socketio

def dev():
    import services

if __name__ == '__main__':
    dev()
    webbrowser.open('http://localhost:5005', autoraise=True)
    socketio.run(app, host='0.0.0.0', port=5005, debug=True)
