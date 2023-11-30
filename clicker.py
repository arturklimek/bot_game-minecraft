import threading
import time
import pyautogui
import keyboard
from app_config import get_autoclicker_delay_ms, get_button_autoclicker_lpm, get_button_autoclicker_ppm
from logger import app_logger

autoclicker_active = {'left': False, 'right': False}

def click_right_mouse_button() -> None:
    """
    Simulates a right mouse button click using the pyautogui library.
    """
    pyautogui.click(button='right')

def click_left_mouse_button() -> None:
    """
    Simulates a left mouse button click using the pyautogui library.
    """
    pyautogui.click(button='left')

def autoclicker(button: str) -> None:
    """
    Runs an autoclicker loop for the specified mouse button.

    The function continuously clicks the specified button at intervals defined by 'get_autoclicker_delay_ms' until the corresponding flag in 'autoclicker_active' is set to False.

    Args:
        button (str): The mouse button for the autoclicker ('left' or 'right').
    """
    app_logger.debug(f"autoclicker was run on button: {button} using delay: {get_autoclicker_delay_ms()}")
    while True:
        if autoclicker_active[button]:
            pyautogui.click(button=button)
            time.sleep(get_autoclicker_delay_ms() / 1000.0)
        else:
            app_logger.debug(f"autoclicker flag was change - stopped on button: {button}")
            break

def toggle_autoclicker(button: str) -> None:
    """
    Toggles the state of the autoclicker for the specified button.

    If the autoclicker for the given button is inactive, it starts it in a new thread.
    If active, it sets the flag to stop the autoclicker.

    Args:
        button (str): The mouse button for which the autoclicker is toggled ('left' or 'right').
    """
    autoclicker_active[button] = not autoclicker_active[button]
    if autoclicker_active[button]:
        thread = threading.Thread(target=autoclicker, args=(button,), daemon=True)
        thread.start()

def setup_autoclicer_hotkeys() -> None:
    """
    Sets up keyboard hotkeys to toggle the left and right mouse button autoclickers.

    The function maps specific keys (retrieved from app configuration) to toggle the state of the left and right mouse button autoclickers.
    """
    global autoclicker_lpm_thread, autoclicker_ppm_thread
    keyboard.add_hotkey(get_button_autoclicker_lpm(), lambda: toggle_autoclicker('left'))
    keyboard.add_hotkey(get_button_autoclicker_ppm(), lambda: toggle_autoclicker('right'))
