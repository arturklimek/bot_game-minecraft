import keyboard

def print_pressed_keys(e):
    """
    Prints the name and scan code of the pressed key.

    This function is triggered every time a keyboard event occurs.
    It prints out the name and scan code of the key that was pressed.

    Args:
        e (keyboard.KeyboardEvent): An event object containing information about the key event.

    Output:
        Information about the pressed key, including its name and scan code, is printed to the console.
    """
    print(f"Button name: {e.name} Button code: {e.scan_code}")

keyboard.hook(print_pressed_keys)
keyboard.wait('esc')