import os
from subprocess import Popen, PIPE
import time
from config import socketio, cmd_list, state_dict

cwd_list = []

def handle_cmd(cmd_step):
    for step in cmd_step:
        #init list and dict
        if step == 0:
            cwd_list = []
        cmd =  cmd_list[step]
        # check first if a cmd is cd
        if cmd[:2] == 'cd':
            for bag in state_dict['selectBag']:
                cwd_list.append(bag)
        elif 'ds-rosbag-scan' in cmd:
            for idx, cwd in enumerate(cwd_list):
                p = Popen(cmd, shell=True, stdout=PIPE, cwd=cwd)
                stdout, err = p.communicate()
                if cwd not in state_dict['bagParamDict']:
                    state_dict['bagParamDict'][cwd] = stdout
