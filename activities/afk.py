import random
import time
from activities.chat import tp_to_spawn
from app_config import get_afk_breaks_flag
from logger import app_logger

afk_counter = None

def weighted_random_choice(values: list, weights: list) -> any:
    """
    Selects a random choice from a list of values, weighted by a corresponding list of weights.

    Args:
        values: A list of possible choices.
        weights: A list of weights corresponding to each value in 'values'.

    Returns:
        A randomly selected value from 'values', chosen based on the distribution defined by 'weights'.
    """
    return random.choices(values, weights=weights, k=1)[0]

def get_afk_counter() -> int:
    """
    Retrieves the current value of the AFK (Away From Keyboard) counter.

    This function returns the value of the global variable 'afk_counter', which tracks the number of times the AFK status has been detected or triggered.

    Returns:
        int: The current value of the AFK counter.
    """
    return afk_counter

def afk() -> bool:
    """
    Simulates an AFK (Away From Keyboard) behavior based on a cofigurable flag and intervals.

    If the AFK breaks flag is enabled, this function will intermittently teleport the player to the spawn and pause the execution for a random duration to simulate AFK behavior.

    Returns:
        True if an AFK action was performed, False otherwise.
    """
    global afk_counter
    if get_afk_breaks_flag():
        app_logger.debug(f"afk_counter: {afk_counter}")
        if afk_counter is None:
            afk_counter = draw_afk_interval()
            app_logger.info(f"afk_counter is None, draw new value: {afk_counter}")
            return False
        else:
            afk_counter = afk_counter - 1
            if afk_counter <= 0:
                time.sleep(5)
                tp_to_spawn()
                time.sleep(5)
                afk_time = draw_afk_time()
                app_logger.info(f"Drawed afk_time: {afk_time}")
                time.sleep(afk_time)
                afk_counter = draw_afk_interval()
                app_logger.info(f"Drawed afk_counter: {afk_counter}")
                return True
            else:
                return False
    else:
        return False

def draw_afk_interval() -> int:
    """
    Determines a random interval for the next AFK action.

    This function generates a weighted random interval, typically used to decide after how many seconds the next AFK simulation should occur.

    Returns:
        A randomly generated integer representing the time interval in seconds until the next AFK action.
    """
    app_logger.debug("draw_afk_interval was used")
    values = list(range(60, 180))
    max_value = 100
    weights = [(max_value - abs(x - max_value)) ** 2 for x in values]
    new_drwa_value = weighted_random_choice(values, weights)
    app_logger.debug(f"new_draw_value: {new_drwa_value}")
    return new_drwa_value

def draw_afk_time() -> int:
    """
    Determines a random duration for the AFK action.

    This function generates a weighted random duration for the AFK action, representing how long the simulated AFK state should last.

    Returns:
        A randomly generated integer representing the duration in seconds of the AFK action.
    """
    app_logger.debug("draw_afk_time was used")
    values = [1, 2, 3, 4, 5]
    weights = [10, 20, 30, 25, 15]
    new_drwa_value = weighted_random_choice(values, weights)*60
    app_logger.debug(f"new_draw_value: {new_drwa_value}")
    return new_drwa_value
