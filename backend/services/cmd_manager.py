import os
import re
import datetime
import logging

from subprocess import Popen, PIPE
from threading import Thread, Semaphore, currentThread
from collections import deque

from config import socketio, cmd_list, state_dict
from ThreadPool import ThreadPool

STEP = 5
OUTPUT_DIR = '~/out'
task_sum = 0
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

def add_one_sec(bag_name):
    ts = datetime.datetime(*map(int, bag_name.split('-')))
    return (ts - datetime.timedelta(seconds=1)).strftime("%Y-%m-%d-%H-%M-%S")

def import_func(cmd, cwd, step):
    global task_sum
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=cwd)
    bag_name = extract_bag_name(cmd)
    if step:
        bag_name = add_one_sec(bag_name)
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
        print 'debug: ', step, bag_name
        state_dict['bagProgDict'][bag_name][step] = color_list[1]
    else:
        state_dict['bagProgDict'][bag_name][step] = color_list[2]
    task_sum -= 1
    socketio.emit('init_state', state_dict)
    if task_sum == 0:
        handle_cmd(step + 1)

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

def cd_and_scan():
    global OUTPUT_DIR
    cwd_list = []
    # working dir
    for bag in state_dict['selectBag']:
        cwd_list.append(bag)
    # scan
    for cwd in cwd_list:
        p = Popen('ds-rosbag-scan-multi ' + OUTPUT_DIR, shell=True, stdout=PIPE, cwd=cwd)
        stdout, err = p.communicate()
        if cwd not in state_dict['bagParamDict']:
            state_dict['bagParamDict'][cwd] = stdout

def handle_cmd(cmd_step):
    global task_sum, OUTPUT_DIR
    cmd =  cmd_list[cmd_step]
    if 'ds-rosbag-import' in cmd:
        for cwd, params in state_dict['bagParamDict'].iteritems():
            for param in params.splitlines():
                bag_name = extract_bag_name(param)
                state_dict['bagProgDict'][bag_name] = [color_list[0]] * STEP
                state_dict['bagTermOutputDict'][bag_name] = []
                task_deque.append((cmd + ' ' + param, cwd, 0))
                task_sum += 1
        execute_in_parallel(task_deque,)
    elif 'ds' in cmd:
        abs_path = os.path.expanduser(OUTPUT_DIR)
        for bag_name in os.listdir(abs_path):
            task_deque.append((cmd + ' ' + bag_name, abs_path, cmd_step))
            task_sum += 1
        execute_in_parallel(task_deque,)
    elif 'cp' in cmd:
        pass
