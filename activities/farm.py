import threading
from typing import Optional, Tuple
import activities.eq_bar
import copy
import time
import keyboard
import pyautogui
from activities.chat import tp_to_farm_home, sellall_inventory, tp_to_spawn, set_tmp_home, tp_to_tmp_home
from activities.eq_bar import get_item_slot_number, get_axe_image, check_axe_damage_to_repair, check_and_update_eq_coordinates
from activities.repair import repair_item
from app_config import get_farm_number, get_farm_floors_number, get_farm_floor_time_moving, \
    get_tmp_home_flag, get_hotkey_moving_left, get_hotkey_moving_right, get_hotkeys_slots
from delay import return_random_wait_interval_time
from logger import app_logger
from screenshooter import get_last_screenshot

axe_slot = 8

farm_procedure_thread = None
is_running_farm_procedure = False

def farm_procedure() -> None:
    """
    Executes the farming procedure for a specified number of farms.

    This function automates the farming process in each farm. It iterates over a set number of farms, performing actions like teleporting to the farm location, using the axe for farming, selling inventory, and repairing the axe if necessary. The procedure includes navigation and interaction controls.

    Globals:
        current_moving_direction (str): The current direction the character is moving in the game.
        is_running_farm_procedure (bool): Flag to check if the farm procedure is currently running.

    Note:
        This function depends on various configuration settings like farm number, floor time moving, and more. It also relies on the state of global variables to manage the flow of the procedure.
    """
    global current_moving_direction
    global is_running_farm_procedure
    app_logger.debug("Starting farm_procedure")
    try:
        if is_running_farm_procedure:
            app_logger.debug(f"farm_number is {get_farm_number()}")
            for farm in range(get_farm_number()):
                repeat_farm = True
                while repeat_farm:
                    repeat_farm = False
                    app_logger.debug(f"repeat_farm was set to {repeat_farm}")
                    if (farm % 2) == 0:
                        current_moving_direction = get_hotkey_moving_left()
                    else:
                        current_moving_direction = get_hotkey_moving_right()
                    app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                    keyboard.press_and_release(get_hotkeys_slots()[9])
                    app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
                    time.sleep(return_random_wait_interval_time(0.5, 1))
                    check_and_update_eq_coordinates()
                    tp_to_farm_home(farm + 1)
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
                    for floor in range(get_farm_floors_number()):
                        keyboard.press_and_release(get_hotkeys_slots()[axe_slot])
                        app_logger.debug(f"Press and release {get_hotkeys_slots()[axe_slot]}")
                        time.sleep(0.2)
                        pyautogui.mouseDown(button='left')
                        app_logger.debug(f"Press mouse left")
                        keyboard.press(current_moving_direction)
                        app_logger.debug(f"Press {current_moving_direction} for {get_farm_floor_time_moving()} secounds")
                        app_logger.debug(f"farm_floor_time_moving is {get_farm_floor_time_moving()}")
                        for _ in range(int(get_farm_floor_time_moving() * 2)):
                            from activities.mine import is_running_mine_procedure
                            if not is_running_mine_procedure and not is_running_farm_procedure:
                                pyautogui.mouseUp(button='left')
                                keyboard.release(current_moving_direction)
                                return
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
                        if ((floor + 1) % 2) == 0:
                            sellall_inventory()
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
                                time.sleep(return_random_wait_interval_time(0.1, 0.75))
                            else:
                                app_logger.debug("Taked check_axe_damage_to_repair is None")
                        else:
                            app_logger.debug(f"Taked axe_image_result is None")
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
