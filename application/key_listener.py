# from pynput import keyboard

# def randdom_func(expected_key):
#     if expected_key == '_':
#         expected_key = 'space'
#     the_key = None
#     def on_press(key):              
#         try:
#             nonlocal the_key
#             the_key = key.char
#             print(f'the key is {key}')
#             return False
#         except AttributeError:
#             the_key = key.name
#             # print(the_key == expected_key)
#             # print('special key was pressed')     
#             return False


#     with keyboard.Listener(
#         on_press=on_press,
#         # on_release=on_release,
#         suppress=False) as listener:
#         listener.join()
#     print(f"The pressed key is: {the_key}, the expected key is: {expected_key}")
#     # print(the_key== expected_key)
#     if the_key== expected_key:
#         return {'result' :True}
#     if the_key == 'esc':
#         return {'result' :'Abort'}
#     else:
#         return {'result' :False}


import keyboard
def k_listener():
    pressed_key = keyboard.read_event()
    if pressed_key.event_type == keyboard.KEY_UP:
        return k_listener()
    return pressed_key.name
