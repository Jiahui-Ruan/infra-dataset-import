from config import socketio, state_dict
from cmd_manager import handle_cmd

@socketio.on('call_init')
def init_state():
    socketio.emit('init_state', state_dict)
    socketio.emit('change_step', state_dict['step'])

@socketio.on('select_bag_change')
def select_bag_change(select_bag_list):
    state_dict['selectBag'] = select_bag_list
    # remove the un-selected bag
    for bag in state_dict['bagParamDict'].keys():
        if bag not in select_bag_list:
            state_dict['bagParamDict'].pop(bag)

@socketio.on('bag_param_change')
def bag_param_change(bag_param_dict):
    state_dict['bagParamDict'] = bag_param_dict

@socketio.on('submit_bag')
def submit_bag():
    handle_cmd((0, 1))

@socketio.on('start_import')
def start_import():
    handle_cmd((2))

@socketio.on('prev_page')
def prev_page():
    state_dict['step'] -= 1
    socketio.emit('change_step', state_dict['step'])
    socketio.emit('init_state', state_dict)

@socketio.on('next_page')
def next_page():
    state_dict['step'] += 1
    socketio.emit('change_step', state_dict['step'])
    socketio.emit('init_state', state_dict)
