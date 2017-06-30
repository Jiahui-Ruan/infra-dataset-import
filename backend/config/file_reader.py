#!/usr/bin/env python
try:
    import yaml
except:
    print "you did not install pyyaml module"

class FileReader:
    def __init__(self):
        self.cmd_list = []

    def _read_file(self, filepath):
        with open(filepath, mode='r') as ymlfile:
            cfg_list = yaml.load(ymlfile)
        for cmd in cfg_list:
            self.cmd_list.append(cmd['cmd'])

    def get_all_cmd(self, filepath):
        self._read_file(filepath)
        return self.cmd_list
