import os
from subprocess import Popen, PIPE, CalledProcessError
import time
from config import socketio, cmd_list, state_dict

cwd_list = []

def execute(cmd, cwd):
    popen = Popen(cmd, stdout=PIPE, universal_newlines=True, shell=True, cwd=cwd)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise CalledProcessError(return_code, cmd)

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
            for cwd in cwd_list:
                p = Popen(cmd, shell=True, stdout=PIPE, cwd=cwd)
                stdout, err = p.communicate()
                if cwd not in state_dict['bagParamDict']:
                    state_dict['bagParamDict'][cwd] = stdout
        elif 'ds-rosbag-import' in cmd:
            for cwd, params in state_dict['bagParamDict'].iteritems():
                for param in params.splitlines():
                    for line in execute(cmd + ' ' + param, cwd):
                        print line
