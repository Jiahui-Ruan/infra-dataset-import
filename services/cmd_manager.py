import os

from config import socketio
from subprocess import Popen, PIPE

pList = []

@socketio.on('sendCmd')
def handleCmd(cmdObj):
    cmd = cmdObj['cmd'] + cmdObj.get('param', '')
    # check first if a cmd is cd
    if cmd[:2] == 'cd':
        os.chdir(cmd[3:])
        print cmd[3:]
        return

    if not pList:
        p = Popen(cmd, shell=True, stdout=PIPE)
    else:
        p = Popen(cmd, shell=True, stdout=PIPE, stdin=pList[-1].stdout)

    pList.append(p)
    stdout, err = p.communicate()
    print stdout
