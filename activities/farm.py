import threading
from typing import Optional, Tuple

import activities.eq_bar
import copy
import time
import keyboard
import pyautogui

from activities.afk import afk_break, get_afk_counter
from activities.chat import tp_to_farm_home, sellall_inventory, tp_to_spawn, set_tmp_home, tp_to_tmp_home
from activities.eq_bar import get_item_slot_number, get_axe_image, check_axe_damage_to_repair, check_and_update_eq_coordinates
from activities.repair import repair_item
from app_config import get_farm_number, get_farm_floors_number, get_farm_floor_time_moving, \
    get_tmp_home_flag, get_hotkey_moving_left, get_hotkey_moving_right, get_hotkeys_slots, get_farm_sell_frequency
from delay import return_random_wait_interval_time
from log_game_processor import get_reply_data, make_reply, check_risk_exit, make_risk_exit, check_risk_afk, \
    make_risk_afk
from logger import app_logger
from screenshooter import get_last_screenshot

axe_slot = 8

farm_procedure_thread = None
is_running_farm_procedure = False

def get_is_running_farm_procedure() -> bool:
    return is_running_farm_procedure

def set_is_running_farm_procedure(new_state) -> None:
    global is_running_farm_procedure
    is_running_farm_procedure = new_state

def make_farm(farm_number) -> bool:
    """
    Executes the farming routine for a specified farm number.

    This function automates the farming process on a given farm instance. It includes selling inventory, updating equipment coordinates, teleporting to specific farm homes, and automating the farm harvest process. The routine adapts the movement direction based on the farm number and handles various checks, such as stopping the process based on certain conditions.

    Args:
        farm_number: The number identifying the specific farm to be automated.

    Returns:
        bool: Returns False, if the faring procedure is interrupted or terminated before time and the further part of the autofarm is not to be continued. Returns True if an error has occurred but the autofarm operation is to continue.

    Raises:
        Exception: If an unexpected error occurs during the farming process.
    """
    global current_moving_direction
    try:
        repeat_farm = True
        while repeat_farm:
            sell_counter = 0
            repeat_farm = False
            app_logger.debug(f"repeat_farm was set to {repeat_farm}")
            if (farm_number % 2) == 0:
                current_moving_direction = get_hotkey_moving_left()
            else:
                current_moving_direction = get_hotkey_moving_right()
            app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
            keyboard.press_and_release(get_hotkeys_slots()[9])
            app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
            time.sleep(return_random_wait_interval_time(0.5, 1))
            check_and_update_eq_coordinates()
            tp_to_farm_home(farm_number + 1)
            time.sleep(return_random_wait_interval_time(0.2, 0.4))
            keyboard.press_and_release(get_hotkeys_slots()[9])
            app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
            time.sleep(return_random_wait_interval_time(0.1, 0.5))
            sellall_inventory()
            time.sleep(return_random_wait_interval_time(0.5, 1))
            change_axe_slot_number()
            time.sleep(return_random_wait_interval_time(0.2, 0.4))
            keyboard.press("shift")
            app_logger.debug(f"Pressing 'shift'")
            keyboard.press_and_release(get_hotkeys_slots()[axe_slot])
            app_logger.debug(f"Press and release {get_hotkeys_slots()[axe_slot]}")
            time.sleep(0.5)
            keyboard.release("shift")
            app_logger.debug(f"Release 'shift'")
            app_logger.debug(f"farm_floors_number is {get_farm_floors_number()}")
            for floor in range(int(get_farm_floors_number())):
                keyboard.press_and_release(get_hotkeys_slots()[axe_slot])
                app_logger.debug(f"Press and release {get_hotkeys_slots()[axe_slot]}")
                time.sleep(0.2)
                pyautogui.mouseDown(button='left')
                app_logger.debug(f"Press mouse left")
                keyboard.press(current_moving_direction)
                app_logger.debug(f"Press {current_moving_direction} for {get_farm_floor_time_moving()} secounds")
                app_logger.debug(f"farm_floor_time_moving is {get_farm_floor_time_moving()}")
                for time_iteration in range(int(get_farm_floor_time_moving() * 2)):
                    from activities.mine import is_running_mine_procedure
                    if not is_running_mine_procedure and not is_running_farm_procedure:
                        pyautogui.mouseUp(button='left')
                        keyboard.release(current_moving_direction)
                        return False
                    if get_reply_data():
                        pyautogui.mouseUp(button='left')
                        app_logger.debug(f"Release mouse left")
                        keyboard.release(current_moving_direction)
                        app_logger.debug(f"Release {current_moving_direction}")
                        time.sleep(1)
                        make_reply()
                        time.sleep(2)
                        if check_risk_exit():
                            time.sleep(1)
                            make_risk_exit()
                            time.sleep(1)
                            set_is_running_farm_procedure(False)
                            return False
                        if check_risk_afk(): #TODO: add other action if get_tmp_home_flag() is used (is True)
                            time.sleep(1)
                            make_risk_afk()
                            time.sleep(1)
                            return True
                        pyautogui.mouseDown(button='left')
                        app_logger.debug(f"Press mouse left")
                        keyboard.press(current_moving_direction)
                        app_logger.debug(f"Press {current_moving_direction}")
                    time.sleep(0.5)
                pyautogui.mouseUp(button='left')
                app_logger.debug(f"Release mouse left")
                keyboard.release(current_moving_direction)
                app_logger.debug(f"Release {current_moving_direction}")
                if current_moving_direction == get_hotkey_moving_right():
                    current_moving_direction = get_hotkey_moving_left()
                elif current_moving_direction == get_hotkey_moving_left():
                    current_moving_direction = get_hotkey_moving_right()
                app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                time.sleep(return_random_wait_interval_time(0.1, 0.5))
                if sell_counter <= get_farm_sell_frequency():
                    sellall_inventory()
                    sell_counter = 0
                else:
                    sell_counter = sell_counter + 1
                time.sleep(return_random_wait_interval_time(0.1, 0.5))
                keyboard.press_and_release(get_hotkeys_slots()[9])
                app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
                time.sleep(return_random_wait_interval_time(0.5, 1))
                last_image = copy.copy(get_last_screenshot())
                check_and_update_eq_coordinates()
                eq_slot_x1, eq_slot_y1 = activities.eq_bar.eq_slot_top_left
                eq_slot_x2, eq_slot_y2 = activities.eq_bar.eq_slot_bottom_right
                cropped_slots_image = last_image[eq_slot_y1:eq_slot_y2, eq_slot_x1:eq_slot_x2]
                axe_image_result = get_axe_image(cropped_slots_image)
                if axe_image_result is not None:
                    cropped_pickaxe_image, axe_top_left, axe_bottom_right = axe_image_result
                    change_axe_slot_number(axe_top_left, axe_bottom_right)
                    if check_axe_damage_to_repair(cropped_pickaxe_image):
                        keyboard.press_and_release(get_hotkeys_slots()[9])
                        app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
                        time.sleep(return_random_wait_interval_time(1, 1.5))
                        check_and_update_eq_coordinates()
                        time.sleep(return_random_wait_interval_time(0.1, 0.5))
                        keyboard.press_and_release(get_hotkeys_slots()[axe_slot])
                        app_logger.debug(f"Press and release {get_hotkeys_slots()[axe_slot]}")
                        time.sleep(return_random_wait_interval_time(0.1, 0.2))
                        if get_tmp_home_flag():
                            app_logger.debug(f"tmp_home_flag {get_tmp_home_flag()}")
                            set_tmp_home()
                            time.sleep(return_random_wait_interval_time(0.2, 0.5))
                            repair_item()
                            time.sleep(return_random_wait_interval_time(0.5, 1))
                            tp_to_tmp_home()
                        else:
                            repair_item()
                            if floor + 1 < get_farm_floors_number():
                                repeat_farm = True
                                app_logger.debug(f"repeat_farm was set to {repeat_farm}")
                                break
                        keyboard.press_and_release(get_hotkeys_slots()[axe_slot])
                        app_logger.debug(f"Press and release {get_hotkeys_slots()[axe_slot]}")
                        time.sleep(return_random_wait_interval_time(1, 1.5))
                    else:
                        app_logger.debug("Taked check_axe_damage_to_repair is None")
                else:
                    app_logger.debug(f"Taked axe_image_result is None")
                if get_tmp_home_flag():
                    app_logger.debug(f"tmp_home_flag {get_tmp_home_flag()}")
                    afk_counter = get_afk_counter()
                    if afk_counter is not None:
                        if get_afk_counter() - 1 <= 0:
                            set_tmp_home()
                            time.sleep(return_random_wait_interval_time(0.2, 0.5))
                            afk_break()
                            time.sleep(return_random_wait_interval_time(0.5, 1))
                            tp_to_tmp_home()
                        else:
                            afk_break()
                    else:
                        afk_break()
                else:
                    if afk_break():
                        if floor + 1 < get_farm_floors_number():
                            repeat_farm = True
                            app_logger.debug(f"repeat_farm was set to {repeat_farm}")
                            break
    except Exception as ex:
        app_logger.error(ex)

def farm_procedure() -> None:
    """
    Manages and coordinates the overall farming procedure.

    This function controls the execution of the farming process over a specified number of farms. It iteratively invokes the make_farm function for each farm. The process checks if the farming procedure should continue or stop based on various conditions, including user-defined settings and in-game occurrences.

    Side effects:
        - Sets the global variable `is_running_farm_procedure` to False if the farming process is interrupted or if a condition for termination is met.

    Raises:
        Exception: If an unexpected error occurs during the farming process.
    """
    global is_running_farm_procedure
    app_logger.debug("Starting farm_procedure")
    try:
        if is_running_farm_procedure:
            app_logger.debug(f"farm_number is {get_farm_number()}")
            for farm in range(int(get_farm_number())):
                if make_farm(farm) is False:
                    is_running_farm_procedure= False
                    return
    except Exception as ex:
        app_logger.error(ex)

def change_axe_slot_number(axe_top_left: Optional[Tuple[int, int]] = None, axe_bottom_right: Optional[Tuple[int, int]] = None) -> None:
    """
    Changes the currently active axe slot number based on its position in the inventory.

    Args:
        axe_top_left (tuple, optional): The top left coordinates of the axe image in the inventory.
        axe_bottom_right (tuple, optional): The bottom right coordinates of the axe image in the inventory.

    If the coordinates are not provided, the function attempts to find the axe image and its position.
    If found, the axe slot number is updated globally.

    Globals:
        axe_slot (int): The current slot number of the axe in the inventory.

    Note:
        This function is used to dynamically update the axe slot number based on its position in the inventory.
    """
    global axe_slot
    if axe_top_left is None or axe_bottom_right is None:
        app_logger.debug(f"axe_top_left: {axe_top_left} OR axe_bottom_right: {axe_bottom_right} is None - try get_axe_image()")
        axe = get_axe_image()
        if axe:
            image_pickaxe, axe_top_left, axe_bottom_right = axe
            app_logger.debug(f"axe_top_left: {axe_top_left} axe_bottom_right: {axe_bottom_right}")
        else:
            app_logger.debug(f"Taked axe is: {axe}")
            return
    new_axe_slot = get_item_slot_number(axe_top_left, axe_bottom_right)
    app_logger.debug(f"new_axe_slot is {new_axe_slot}")
    if new_axe_slot != axe_slot:
        app_logger.debug(f"axe_slot: {axe_slot} changing to new_axe_slot: {new_axe_slot}")
        axe_slot = new_axe_slot
    else:
        app_logger.debug("axe_slot and new_axe_slot are that same")

def farm_procedure_loop() -> None:
    """
    Continuously runs the farm procedure while the farming process is active.

    This loop ensures that the farming procedure is executed continuously as long as the `is_running_farm_procedure` global variable is True. It handles teleportation to the spawn point and initiates the farming procedure.

    Globals:
        is_running_farm_procedure (bool): Flag to check if the farm procedure is currently running.

    Note:
        This function acts as a controlling loop for the farming process, managing its continuous execution.
    """
    global is_running_farm_procedure
    app_logger.debug("Starting farm_procedure_loop")
    while is_running_farm_procedure:
        time.sleep(1)
        tp_to_spawn()
        time.sleep(return_random_wait_interval_time(1, 3))
        farm_procedure()

def toggle_farm_procedure() -> None:
    """
    Toggles the farming procedure on or off based on the current state.

    This function initiates or stops the farm procedure based on its current state. If the farming procedure
    is not running, it starts a new thread for the farm procedure loop. Otherwise, it stops the procedure.

    Globals:
        is_running_farm_procedure (bool): Flag indicating whether the farm procedure is currently running.
        farm_procedure_thread (threading.Thread): The thread running the farm procedure loop.

    Note:
        This function checks if any other procedures like mining are running before starting the farming process.
    """
    global is_running_farm_procedure
    global farm_procedure_thread
    from activities.mine import is_running_mine_procedure
    if is_running_mine_procedure:
        app_logger.info(f"Can not start farm procedure - other procedure is running")
    else:
        is_running_farm_procedure = not is_running_farm_procedure
        state = 'started' if is_running_farm_procedure else 'stopped'
        app_logger.info(f"Farm procedure {state}")
        print(f"Farm procedure {state}")
        if is_running_farm_procedure:
            if farm_procedure_thread is None or not farm_procedure_thread.is_alive():
                farm_procedure_thread = threading.Thread(target=farm_procedure_loop)
                farm_procedure_thread.start()
