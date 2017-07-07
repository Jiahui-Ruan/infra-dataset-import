import os
import re
import logging

from subprocess import Popen, PIPE
from threading import Thread, Semaphore, currentThread
from collections import deque

from config import socketio, cmd_list, state_dict
from ThreadPool import ThreadPool

STEP = 5
output_dir = None
color_list = [
    '#e6ffe6',
    '#21ba45',
    '#db2828',
    '#fbbd08',
    '#2185d0'
]

cwd_list = []
task_deque = deque()

def extract_bag_name(cmd):
    for param in cmd.split():
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', param)
        if match:
            return match.group(0)

def import_func(cmd, cwd, step):
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=cwd)
    bag_name = extract_bag_name(cmd)
    out_str = ""
    while p.poll() is None:
        c = p.stdout.read(1)
        if not c:
            c = p.stderr.read(1)
        if c != '\n':
            out_str += c
        else:
            state_dict['bagTermOutputDict'][bag_name].append(out_str)
            state_dict['bagProgDict'][bag_name][step] = color_list[4]
            socketio.emit('init_state', state_dict)
            out_str = ""
    if p.returncode == 0:
        state_dict['bagProgDict'][bag_name][step] = color_list[1]
    else:
        state_dict['bagProgDict'][bag_name][step] = color_list[2]
    socketio.emit('init_state', state_dict)

def import_worker(s, pool, cmd, cwd, step):
    logging.debug('Waiting to join the pool')
    cmd = 'PYTHONUNBUFFERED=1 ' + cmd
    with s:
        name = currentThread().getName()
        pool.makeActive(name)
        import_func(cmd, cwd, step)
        pool.makeInactive(name)

def execute_in_parallel(task_deque):
    s = Semaphore(5)
    pool = ThreadPool()
    task = None
    while task_deque:
        task = task_deque.popleft()
        t = Thread(target=import_worker, args=[s, pool, task[0], task[1], task[2]])
        t.setDaemon(True)
        t.start()
    # handle_cmd((task[2] + 4,))

def determine_progress(cmd):
    if 'compress-video' in cmd:
        return 1
    elif 'check' in cmd:
        return 2
    elif 'cp' in cmd:
        return 3
    elif 'submit' in cmd:
        return 4

def handle_cmd(cmd_step):
    for step in cmd_step:
        cmd =  cmd_list[step]
        # check first if a cmd is cd
        if step == 0:
            cwd_list = []
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
                    bag_name = extract_bag_name(param)
                    # init two dict for recording
                    state_dict['bagProgDict'][bag_name] = [color_list[0]] * STEP
                    state_dict['bagTermOutputDict'][bag_name] = []
                    task_deque.append((cmd + ' ' + param, cwd, 0))
            execute_in_parallel(task_deque,)
        elif step == 3:
            output_dir = cmd.split()[1]
        elif 'ds' in cmd:
            progress = determine_progress(cmd)
            abs_path = os.path.expanduser(output_dir)
            for bag_name in os.listdir(abs_path):
                task_deque.append((cmd + ' ' + bag_name, abs_path, progress))
            execute_in_parallel(task_deque,)
        elif 'cp' in cmd:
            pass
