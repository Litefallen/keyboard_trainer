from pynput import keyboard


def randdom_func(expected_key):
    if expected_key == '_':
        expected_key = 'space'
    the_key = None
    print(expected_key)
    def on_press(key):
        try:
            nonlocal the_key
            the_key = key.char
            print(f'the key is {key}')
            return False
        except AttributeError:
            the_key = key.name
            print(the_key == expected_key)
            if key.name == 'esc':
                exit()
            print(key.name)
            return False

    with keyboard.Listener(
        on_press=on_press,
        # on_release=on_release,
        suppress=True) as listener:
        listener.join()
    print(f"The pressed key is: {the_key}, the expected key is: {expected_key}")
    print(the_key== expected_key)
    return {'result' :True} if the_key== expected_key else {'result' :False}
