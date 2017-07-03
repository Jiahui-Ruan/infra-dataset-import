import os
import getpass
import fnmatch

from config import socketio, state_dict

@socketio.on('find_bags')
def find_bags():
    matches = []
    for root, dirnames, filenames in os.walk('/media/{}'.format(getpass.getuser())):
        for filename in fnmatch.filter(filenames, '*.bag'):
            path = os.path.join(root.rsplit('/',1)[0])
            if path not in matches:
                matches.append(path)
            break
    state_dict['allBag'] = matches
    socketio.emit('all_bag_found', matches)

@socketio.on('umount_ssd')
def umount_ssd():
    pass
