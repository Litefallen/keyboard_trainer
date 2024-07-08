import keyboard
def k_listener():
    pressed_key = keyboard.read_event()
    if pressed_key.event_type == keyboard.KEY_UP:
        return k_listener()
    return pressed_key.name
