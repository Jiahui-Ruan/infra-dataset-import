from config import socketio, state_dict

@socketio.on('call_init')
def init_state():
    socketio.emit('init_state', state_dict)

@socketio.on('select_bag_change')
def select_bag_change(select_bag_list):
    state_dict['selectBag'] = select_bag_list
