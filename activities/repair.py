import threading
import time
from activities.chat import tp_to_repair_home
from clicker import click_right_mouse_button
from delay import return_random_wait_interval_time
from logger import app_logger


def repair_item() -> None:
    """
    Initiates the item repair procedure.

    This function automates the process of repairing an item by teleporting to the repair home, waiting for a random interval, and then performing a series of right mouse button clicks to interact with the necessary game interface for repairing.

    Note:
        The function includes multiple time.sleep() calls with random intervals to mimic human-like interactions and avoid detection in the game environment.
    """
    app_logger.debug("repair_item procedure was started")
    time.sleep(return_random_wait_interval_time(0.5,1.5))
    tp_to_repair_home()
    time.sleep(return_random_wait_interval_time(1.5,3))
    for x in range(3):
        time.sleep(return_random_wait_interval_time())
        click_right_mouse_button()
    time.sleep(return_random_wait_interval_time(1, 2))

def repair_item_thread() -> None:
    """
    Starts a new thread to execute the item repair procedure.

    This function creates and starts a new thread dedicated to running the repair_item function.
    It allows the repair process to run independently of the main program flow, ensuring that the application remains responsive.

    Note:
        The use of threading ensures that the application's main thread is not blocked while the repair process is ongoing.
    """
    threading.Thread(target=repair_item).start()
