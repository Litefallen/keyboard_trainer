from pynput import keyboard
import timeit


def randdom_func(expected_key):
    the_key = None
    # expected_key = 'i'
    def on_press(key):
        try:
            nonlocal the_key
            the_key = key.char
            if key == keyboard.Key.esc:
                return 'stopit'
            # print(f'the key is {key}')
            return False
        except AttributeError:
            print(f'special key {key} pressed')

    # def on_release(key):
    #     if key == keyboard.Key.esc:
    #         # Stop listener
    #         return 'stopit'

    with keyboard.Listener(
        on_press=on_press,
        # on_release=on_release,
        suppress=True) as listener:
        listener.join()
    print(f"The pressed key is: {the_key}, the expected key is: {expected_key}")
    print(the_key== expected_key)
    return {'result' :True} if the_key== expected_key else {'result' :False}
# for i in 'zealoft':
#     randdom_func(i)