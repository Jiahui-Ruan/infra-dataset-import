from config import socketio
from subprocess import check_output


@socketio.on('sendCmd')
def handleCmd(cmdObj):
    cmd = cmdObj['cmd'] + cmdObj.get('param', '')
    print cmd
    out = check_output(cmd, shell=True)
    print out
