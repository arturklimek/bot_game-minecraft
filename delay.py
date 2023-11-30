import random
from logger import app_logger

def return_random_wait_interval_time(down: float = 0.15, up: float = 0.3) -> float:
    """
    Generates a random waiting time within a specified interval.

    This function uses a uniform distribution to draw a random floating-point number in the range [down, up], inclusive.

    Args:
        down (float, optional): The lower bound of the interval. Defaults to 0.15.
        up (float, optional): The upper bound of the interval. Defaults to 0.3.

    Returns:
        float: A randomly drawn time interval value within the specified range.
    """
    drawed_time = random.uniform(down, up)
    app_logger.debug(f"return_random_wait_interval_time draw value ({down} - {up}): {drawed_time}")
    return drawed_time
