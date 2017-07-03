from config import socketio, state_dict

@socketio.on('call_init')
def init_state():
    socketio.emit('init_state', state_dict)
    socketio.emit('change_step', state_dict['step'])

@socketio.on('select_bag_change')
def select_bag_change(select_bag_list):
    state_dict['selectBag'] = select_bag_list

@socketio.on('submit_bag')
def submit_bag():
    pass

@socketio.on('prev_page')
def submit_bag():
    state_dict['step'] -= 1
    socketio.emit('change_step', state_dict['step'])
    socketio.emit('init_state', state_dict)

@socketio.on('next_page')
def submit_bag():
    state_dict['step'] += 1
    socketio.emit('change_step', state_dict['step'])
    socketio.emit('init_state', state_dict)
