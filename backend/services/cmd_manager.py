import os
import re
import logging

from subprocess import Popen, PIPE
from threading import Thread, Semaphore, currentThread
from collections import deque

from config import socketio, cmd_list, state_dict
from ThreadPool import ThreadPool

STEP = 5

cwd_list = []
task_deque = deque()

def extract_bag_name(cmd):
    for param in cmd.split():
        match = re.search(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', param)
        if match:
            return match.group(0)

def worker(s, pool, cmd, cwd):
    logging.debug('Waiting to join the pool')
    cmd = 'PYTHONUNBUFFERED=1 ' + cmd
    with s:
        name = currentThread().getName()
        pool.makeActive(name)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=cwd)
        bag_name = extract_bag_name(cmd)
        out_str = ""
        while p.poll() is None:
            c = p.stdout.read(1)
            if c != '\n':
                out_str += c
            else:
                socketio.emit('cmd_output', {bag_name: out_str})
                out_str = ""
        print p.returncode
        state_dict['bagProgDict'][bag_name][0] = p.returncode
        socketio.emit('init_state', state_dict)
        pool.makeInactive(name)

def execute_in_parallel(task_deque):
    s = Semaphore(5)
    pool = ThreadPool()
    while task_deque:
        task = task_deque.popleft()
        t = Thread(target=worker, args=[s, pool, task[0], task[1]])
        t.setDaemon(True)
        t.start()

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
                    bag_name = extract_bag_name(param)
                    # init two dict for recording
                    state_dict['bagProgDict'][bag_name] = [-1] * STEP
                    state_dict['bagTermOutputDict'][bag_name] = []
                    task_deque.append((cmd + ' ' + param, cwd))
            execute_in_parallel(task_deque,)
