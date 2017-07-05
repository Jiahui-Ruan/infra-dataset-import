import os
from subprocess import Popen, PIPE
import time
from config import socketio, cmd_list, pipe_list, state_dict

cwd_list = []

def handle_cmd(cmd_step):
    for step in cmd_step:
        #init list and dict
        if step == 0:
            cwd_list = []
            pipe_list = []
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
                if cwd.rsplit('/', 1)[1] not in state_dict['bagParamDict']:
                    state_dict['bagParamDict'][cwd.rsplit('/', 1)[1]] = stdout
