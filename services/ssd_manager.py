import os
import getpass
import fnmatch

from config import socketio

@socketio.on('find_bags')
def find_bags():
    matches = []
    for root, dirnames, filenames in os.walk('/media/{}'.format(getpass.getuser())):
        for filename in fnmatch.filter(filenames, '*.bag'):
            matches.append(os.path.join(root))
            # after found one .bag jump to next loop
            break
    socketio.emit('all_bag_found', matches)

@socketio.on('umount_ssd')
def umount_ssd():
    pass
