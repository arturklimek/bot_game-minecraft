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

def afk_break() -> bool:
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
                afk_time = draw_break_afk_time()
                afk_on_spawn(afk_time)
                afk_counter = draw_afk_interval()
                app_logger.info(f"Drawed afk_counter: {afk_counter}")
                return True
            else:
                return False
    else:
        return False

def afk_on_spawn(afk_time: int = 0) -> None:
    """
    Executes an AFK (Away From Keyboard) routine on the spawn location in the game.

    This function teleports the player to the game's spawn location and keeps them AFK for a specified duration.
    The function waits for a brief period before and after teleporting to ensure smooth execution of the command.
    It is primarily used to avoid in-game idle detection mechanisms by simulating player activity.

    Args:
        afk_time (int): The time in seconds to remain AFK at the spawn location. Defaults to 0 seconds.
    """
    time.sleep(2)
    tp_to_spawn()
    time.sleep(5)
    app_logger.info(f"Sleep for afk_time: {afk_time}")
    time.sleep(afk_time)

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

def draw_afk_time(values: list, weights: list) -> int:
    """
    Determines a random duration for the AFK action.

    This function generates a weighted random duration for the AFK action, representing how long the simulated AFK state should last.

    Returns:
        A randomly generated integer representing the duration in seconds of the AFK action.
    """
    app_logger.debug(f"draw_afk_time was used - values: {values} weights: {weights}")
    new_drwa_value = weighted_random_choice(values, weights)*60
    app_logger.debug(f"new_draw_value: {new_drwa_value}")
    return new_drwa_value

def draw_break_afk_time() -> int:
    """
    Randomly selects a break AFK time based on predefined values and their respective weights.

    This function uses a weighted random selection to choose a break AFK time from a set of predefined values.
    Each value represents the time in minutes and has an associated weight that determines its selection probability.

    Returns:
        int: A randomly selected break AFK time in minutes.
    """
    values = [1, 2, 3, 4, 5]
    weights = [10, 20, 30, 25, 15]
    return draw_afk_time(values, weights)

def draw_risk_afk_time() -> int:
    """
    Randomly selects a risk AFK time based on a set of values and their corresponding weights.

    This function uses a weighted random selection to choose a risk AFK time from a predefined list of values.
    The values represent the time in minutes and are weighted to influence their probability of being selected.

    Returns:
        int: A randomly selected risk AFK time in minutes, based on weighted probabilities.
    """
    values = [10, 12, 14, 16, 18, 20, 22, 24, 30]
    weights = [10, 12, 14, 17, 14, 12, 10, 8, 3]
    return draw_afk_time(values, weights)
