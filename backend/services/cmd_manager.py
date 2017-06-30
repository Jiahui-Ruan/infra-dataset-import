import os

from config import socketio
from subprocess import Popen, PIPE

pList = []

@socketio.on('sendCmd')
def handleCmd(cmdObj):
    cmd = cmdObj['cmd'] + cmdObj.get('param', '')
    # check first if a cmd is cd
    if cmd[:2] == 'cd':
        try:
            os.chdir(cmd[3:])
            socketio.emit('terminal_rst', {'msg':
                                        'has cd into {}'.format(cmd[3:])})
        except:
            socketio.emit('terminal_rst', {'msg':
                                        'can not cd into {}'.format(cmd[3:])})
        return

    if not pList:
        p = Popen(cmd, shell=True, stdout=PIPE)
    else:
        p = Popen(cmd, shell=True, stdout=PIPE, stdin=pList[-1].stdout)

    pList.append(p)
    stdout, err = p.communicate()
    print stdout
