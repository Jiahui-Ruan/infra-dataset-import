from config import app, socketio

def dev():
    import services

if __name__ == '__main__':
    dev()
    socketio.run(app, host='0.0.0.0', port=5005, debug=True)
