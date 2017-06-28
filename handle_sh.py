#!/usr/bin/env python

class FileReader:

    def __init__(self):
        self.cmd_list = []

    def _read_file(self, filepath):
        with open(filepath, mode='r') as f:
            for line in f:
                if line.startswith('#'):
                    next(f)
                else:
                    self.cmd_list.append(line)

    def get_all_cmd(self, filepath):
        self._read_file(filepath)
        return self.cmd_list
