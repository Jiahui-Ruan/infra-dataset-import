import os
from subprocess import Popen, PIPE
from multiprocessing import Process

from config import socketio, cmd_list, state_dict

process_dict = {}
pList = []

def handleCmd(cmd_step):
    for step in cmd_step:
        cmd =  cmd_list[step]
        # check first if a cmd is cd
        if cmd[:2] == 'cd':
            for bag in state_dict['selectBag']:
                process_dict[bag] = Process(target=os.chdir,
                                                args=(bag,))
                process_dict[bag].start()
                process_dict[bag].join()
            # except:
                # socketio.emit('terminal_rst', {'msg':
                #                             'can not cd into {}'.format(cmd[3:])})
            # return
        # if not pList:
        #     p = Popen(cmd, shell=True, stdout=PIPE)
        # else:
        #     p = Popen(cmd, shell=True, stdout=PIPE, stdin=pList[-1].stdout)
        #
        # pList.append(p)
        # stdout, err = p.communicate()
        # print stdout
