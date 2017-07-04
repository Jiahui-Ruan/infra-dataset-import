import os
from subprocess import Popen, PIPE
import time
from config import socketio, cmd_list, pipe_list, state_dict

cwd_list = []
bag_param_dict = {}

def handle_cmd(cmd_step):
    for step in cmd_step:
        cmd =  cmd_list[step]
        # check first if a cmd is cd
        if cmd[:2] == 'cd':
            for bag in state_dict['selectBag']:
                cwd_list.append(bag)
        else:
            for idx, cwd in enumerate(cwd_list):
                p = Popen(cmd, shell=True, stdout=PIPE, cwd=cwd,
                    stdin=pipe_list[idx].stdout if idx < len(pipe_list) else None)
                pipe_list.append(p)
                stdout, err = p.communicate()
                bag_param_dict[cwd.rsplit('/', 1)[1]] = stdout
            print bag_param_dict
            socketio.emit('bag_param_change', bag_param_dict)
