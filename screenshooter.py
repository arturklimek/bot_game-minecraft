import threading
import time
import mss
import numpy as np
import pygetwindow
from app_config import get_game_window_name, get_screenshots_frequency
from image_operations import convert_screenshot_for_opencv
from logger import app_logger
from typing import Optional, Union

last_screenshoot: Optional[np.ndarray] = None #TODO: change variables and functions from screenshot to screenshoot

def set_last_screenshoot(new_last_screensh0ot: Optional[np.ndarray] = None) -> None:
    global last_screenshoot
    if new_last_screensh0ot is not None:
        last_screenshoot = new_last_screensh0ot

def get_last_screenshot() -> Optional[np.ndarray]:
    """
    Retrieves the last captured screenshot.

    Returns:
        The last screenshot captured by the application.
    """
    app_logger.debug("get_last_screenshot return last_screenshoot")
    return last_screenshoot

def get_screenshot(window_title: str = get_game_window_name()) -> Optional[np.ndarray]:
    """
    Captures a screenshot of a specified window.

    Args:
        window_title (str): The title of the window to capture.
                            Defaults to the game window name from the app configuration.

    Returns:
        The captured screenshot converted for OpenCV processing or None if the window is not active.
    """
    with mss.mss() as sct:
        try:
            window = pygetwindow.getWindowsWithTitle(window_title)[0]
            if window.isActive:
                bbox = window.left, window.top, window.right, window.bottom
                screenshot = sct.grab(bbox)
                converted_screenshoot = convert_screenshot_for_opencv(screenshot)
                return converted_screenshoot
            else:
                app_logger.debug("The window is not active")
        except IndexError:
            app_logger.error(f"Window '{window_title}' not found.")
            return None

def screenshot_loop() -> None:
    """
    Continuously captures screenshots of the specified window at set intervals.

    This function runs in an infinite loop, capturing screenshots and updating the global 'last_screenshot' variable.
    """
    # global last_screenshoot
    time.sleep(1)
    while True:
        try:
            screenshot = get_screenshot(get_game_window_name())
            if screenshot is not None:
                # last_screenshoot = screenshot
                set_last_screenshoot(screenshot)
            else:
                app_logger.debug(f"No screenshot taken for window '{get_game_window_name()}'")
            time.sleep(get_screenshots_frequency())
        except Exception as ex:
            app_logger.error(ex)

def start_screenshot_thread() -> None:
    """
    Starts a new thread for the screenshot loop.

    This function initiates the screenshot capturing process in a separate thread, allowing the application to continue running other tasks simultaneously.
    """
    threading.Thread(target=screenshot_loop, daemon=True).start()
