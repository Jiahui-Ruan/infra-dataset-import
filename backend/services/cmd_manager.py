import os
import logging

from subprocess import Popen, PIPE
from threading import Thread, Semaphore, currentThread
from collections import deque

from config import socketio, cmd_list, state_dict
from ThreadPool import ThreadPool

cwd_list = []
task_deque = deque()

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def worker(s, pool, cmd, cwd):
    logging.debug('Waiting to join the pool')
    with s:
        name = currentThread().getName()
        pool.makeActive(name)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, bufsize=1, shell=True, cwd=cwd)
        while p.poll() is None:
            pass
        print('Not sleeping any longer.  Exited with returncode %d' % p.returncode)
        pool.makeInactive(name)

def execute_in_parallel(task_deque):
    s = Semaphore(4)
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
                    task_deque.append((cmd + ' ' + param, cwd))
            execute_in_parallel(task_deque,)
