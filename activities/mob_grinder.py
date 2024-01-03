import copy
import datetime
import random
import threading
from typing import Optional, Tuple
import keyboard
import pyautogui
from activities.afk import afk_break, afk_on_spawn, draw_risk_afk_time
from activities.chat import tp_to_spawn, tp_to_mobgrinder_home, send_on_chat, send_random_message_coordinates_problem, \
    send_chat_notification
from activities.chest import items_stored_procedure
from activities.eq_bar import get_eq_slot_top_left, get_eq_slot_bottom_right, get_item_slot_number, \
    check_and_update_eq_coordinates, get_sword_image, check_sword_damage_to_repair
from activities.equipment import check_inventory_full
from activities.incubator import restoring_incubator_procedure
from activities.mine import random_double_move_mouse
from activities.repair import repair_item
from app_config import get_coordinates_screen_XYZ_analysis_flag, get_grinder_coordinate_range, get_hotkeys_slots, \
    get_hotkey_moving_up
from coordinate_analyzer import get_coordinates_XYZ, check_coordinates_compatibility_XYZ
from delay import return_random_wait_interval_time
from log_game_processor import get_reply_data, make_reply, check_risk_exit, make_risk_exit, check_risk_afk, \
    make_risk_afk
from logger import app_logger
import time
from screenshooter import get_last_screenshot

grinder_procedure_thread = None
is_running_grind_procedure = False

def get_is_running_grind_procedure() -> bool:
    return is_running_grind_procedure

def set_is_running_grind_procedure(new_state: bool = False) -> None:
    global is_running_grind_procedure
    is_running_grind_procedure = new_state

attacks_number_in_iteration = 60

min_atack_interval = 0.4
max_atack_interval = 1.5

sword_slot = 1

def get_sword_slot() -> int:
    return sword_slot

def set_sword_slot(new_slot: int = sword_slot) -> None:
    global sword_slot
    sword_slot = new_slot


last_iteration_time = datetime.datetime.now()

def get_last_iteration_time() -> datetime.datetime:
    return last_iteration_time

def set_last_iteration_time(new_time: datetime.datetime) -> None:
    global last_iteration_time
    last_iteration_time = new_time

last_coordinates = {}

def get_last_coordinates() -> dict:
    return last_coordinates

def set_last_coordinates(new_coordinates: dict = {}) -> None:
    global last_coordinates
    last_coordinates = new_coordinates

max_coordinates_without_data = 4
max_coordinates_out_of_range = 2

coordinates_without_data = 0
coordinates_out_of_range = 0

def grind_procedure() -> bool:
    """
    Executes the grinding procedure for a specific in-game activity.

    This function automates a series of actions like pressing hotkeys, changing equipment, and attacking,
    in a loop until certain conditions are met (e.g., inventory is full or sword needs repair).

    Returns:
        bool: True if the procedure completes without interruption, False otherwise.
    """
    try:
        app_logger.debug("Start grind_procedure")
        keyboard.press_and_release(get_hotkeys_slots()[9])
        app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
        time.sleep(return_random_wait_interval_time(0.5, 1))
        app_logger.debug(f"Pressing 'shift'")
        keyboard.press("shift")
        keyboard.press(get_hotkey_moving_up())
        time.sleep(1)
        keyboard.release(get_hotkey_moving_up())
        app_logger.debug(f"Release 'shift'")
        keyboard.release("shift")
        repeat_grind = True
        while repeat_grind:
            keyboard.press_and_release(get_hotkeys_slots()[9])
            app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
            time.sleep(return_random_wait_interval_time(0.5, 1))
            check_and_update_eq_coordinates()
            time.sleep(return_random_wait_interval_time(0.5, 1))
            change_sword_slot_number()
            time.sleep(return_random_wait_interval_time(0.2, 0.4))
            app_logger.debug(f"Press and release {get_hotkeys_slots()[get_sword_slot()]}")
            keyboard.press_and_release(get_hotkeys_slots()[get_sword_slot()])
            for iteration in range(attacks_number_in_iteration):
                pyautogui.click(button='left')
                if not get_is_running_grind_procedure():
                    app_logger.debug("is not is_running_grind_procedure - return False")
                    return False
                if not check_and_reply_messages():
                    app_logger.debug("not check_and_reply_messages() - return False")
                    return False
                if not check_coordinates():
                    app_logger.debug("not check_coordinates() - return False")
                    return False
                time.sleep(random.uniform(min_atack_interval, max_atack_interval))
            inventory_status = check_inventory_full()
            if inventory_status:
                app_logger.info("EQ inventory is full.")
                break
            if repair_sword():
                app_logger.info("Sword need repair.")
                break
        return True
    except Exception as ex:
        app_logger.error(ex)

def repair_sword() -> bool:
    """
    Checks and performs the repair of the sword if necessary.

    This function takes a screenshot of the equipment slots, identifies the sword, checks its damage level,
    and performs a repair action if the damage exceeds a certain threshold.

    Returns:
        bool: True if the sword was repaired, False otherwise.
    """
    try:
        app_logger.debug("Start repair_sword")
        app_logger.info(datetime.datetime.now())
        time.sleep(return_random_wait_interval_time(0.1, 0.5))
        app_logger.debug(f"Press and release {get_hotkeys_slots()[9]}")
        keyboard.press_and_release(get_hotkeys_slots()[9])
        time.sleep(return_random_wait_interval_time(0.5, 1))
        last_image = copy.copy(get_last_screenshot())
        check_and_update_eq_coordinates()
        eq_slot_x1, eq_slot_y1 = get_eq_slot_top_left()
        eq_slot_x2, eq_slot_y2 = get_eq_slot_bottom_right()
        cropped_slots_image = last_image[eq_slot_y1:eq_slot_y2, eq_slot_x1:eq_slot_x2]
        sword_image_result = get_sword_image(cropped_slots_image)
        if sword_image_result is not None:
            cropped_pickaxe_image, axe_top_left, axe_bottom_right = sword_image_result
            change_sword_slot_number(axe_top_left, axe_bottom_right)
            if check_sword_damage_to_repair(cropped_pickaxe_image):
                time.sleep(return_random_wait_interval_time(0.1, 0.5))
                app_logger.debug(f"Press and release {get_hotkeys_slots()[get_sword_slot()]}")
                keyboard.press_and_release(get_hotkeys_slots()[get_sword_slot()])
                time.sleep(return_random_wait_interval_time(0.1, 0.2))
                repair_item()
                app_logger.debug("The sword was repaired - return True")
                return True
            else:
                app_logger.debug("Taked check_sword_damage_to_repair is None or False")
        else:
            app_logger.debug(f"Taked sword_image_result is None")
        app_logger.debug(f"The sword has not been repaired - return False")
        return False
    except Exception as ex:
        app_logger.error(ex)

def change_sword_slot_number(sword_top_left: Optional[Tuple[int, int]] = None, sword_bottom_right: Optional[Tuple[int, int]] = None) -> None:
    """
    Updates the slot number of the sword based on its position in the equipment slots.

    Args:
        sword_top_left (Optional[Tuple[int, int]]): The top-left coordinate of the sword.
        sword_bottom_right (Optional[Tuple[int, int]]): The bottom-right coordinate of the sword.

    If the coordinates are not provided, the function attempts to find the sword in the slots and update its slot number.
    """
    try:
        app_logger.debug("Start change_sword_slot_number")
        if sword_top_left is None or sword_bottom_right is None:
            app_logger.debug(
                f"sword_top_left: {sword_top_left} OR sword_bottom_right: {sword_bottom_right} is None - try get_sword_image()")
            axe = get_sword_image()
            if axe:
                image_sword, sword_top_left, sword_bottom_right = axe
                app_logger.debug(f"sword_top_left: {sword_top_left} sword_bottom_right: {sword_bottom_right}")
            else:
                app_logger.debug(f"Taked sword is: {axe}")
                return
        new_sword_slot = get_item_slot_number(sword_top_left, sword_bottom_right)
        app_logger.debug(f"new_sword_slot is {new_sword_slot}")
        if new_sword_slot != get_sword_slot():
            app_logger.debug(f"sword_slot: {get_sword_slot()} changing to new_sword_slot: {new_sword_slot}")
            set_sword_slot(new_sword_slot)
        else:
            app_logger.debug("sword_slot and new_sword_slot are that same")
    except Exception as ex:
        app_logger.error(ex)

def check_coordinates() -> bool:
    """
    Verifies if the current in-game coordinates match the expected range.

    The function checks the player's current coordinates against a predefined range and performs
    actions based on whether the coordinates are within the range, such as sending messages or moving the player.

    Returns:
        bool: True if coordinates are within the expected range, False if actions need to be taken due to deviation.
    """
    try:
        app_logger.debug("Start check_coordinates")
        global coordinates_without_moving
        global coordinates_without_data
        global coordinates_out_of_range
        if get_coordinates_screen_XYZ_analysis_flag():
            app_logger.debug("get_coordinates_screen_XYZ_analysis_flag() is True")
            current_time = datetime.datetime.now()
            time_difference = current_time - get_last_iteration_time()
            if time_difference.total_seconds() < 1:
                app_logger.debug("Less than 1 second has passed since the last iteration")
            else:
                coordinates_range = get_grinder_coordinate_range()
                app_logger.debug(f"coordinates_range: {coordinates_range}")
                current_coordinates = get_coordinates_XYZ()
                coordinate_state = check_coordinates_compatibility_XYZ(coordinates_range, current_coordinates)
                if coordinate_state is False:
                    coordinates_without_data = 0
                    coordinates_out_of_range = coordinates_out_of_range + 1
                    app_logger.debug(
                        f"coordinate_state is {coordinate_state}, set coordinates_out_of_range to value: {coordinates_out_of_range}")
                    pass
                elif coordinate_state is True:
                    coordinates_without_data = 0
                    coordinates_out_of_range = 0
                    app_logger.debug(
                        f"coordinate_state is {coordinate_state} - SET coordinates_without_data: {coordinates_without_data} and coordinates_out_of_range: {coordinates_out_of_range}")
                    pass
                else:
                    coordinates_without_data = coordinates_without_data + 1
                    app_logger.debug(
                        f"coordinate_state is {coordinate_state} - set coordinates_without_data to value: {coordinates_without_data}")
                if coordinates_without_data > max_coordinates_without_data:
                    app_logger.warning(
                        f"coordinates_without_data: {coordinates_without_data} exceeded the max value: {max_coordinates_without_data}")
                    time.sleep(1)
                    send_random_message_coordinates_problem()
                    afk_time = draw_risk_afk_time()
                    app_logger.info(f"Go AFK on spawn (too many coordinates without data) for afk_time: {afk_time}")
                    afk_on_spawn(afk_time)
                    app_logger.debug("AFK time over")
                    time.sleep(1)
                    return False
                if coordinates_out_of_range > max_coordinates_out_of_range:
                    app_logger.warning(
                        f"coordinates_out_of_range: {coordinates_out_of_range} exceeded the max value: {max_coordinates_out_of_range}")
                    random_double_move_mouse()
                    time.sleep(1)
                    send_random_message_coordinates_problem()
                    app_logger.info(f"Go to Lobby (too many coordinates out of range)")
                    go_lobby_exit_mobgrinder()
                    return False
                set_last_coordinates(current_coordinates)
                set_last_iteration_time(current_time)
        app_logger.debug("check_coordinates - return True")
        return True
    except Exception as ex:
        app_logger.error(ex)

def go_lobby_exit_mobgrinder() -> None:
    """
    Exits the mob grinder and returns to the main lobby.

    This function sends a command to return to the game lobby and updates the state of the grinding procedure.
    """
    lobby_command = "/lobby 1"
    time.sleep(1)
    app_logger.info(f"Go to Lobby - execute command: {lobby_command}")
    send_on_chat(lobby_command)
    time.sleep(5)
    set_is_running_grind_procedure(False)

def check_and_reply_messages() -> bool:
    """
    Checks for pending messages and replies if necessary.

    This function handles any pending communication or actions that need to be taken based on game messages,
    such as replying, checking for risks, and adjusting the procedure accordingly.

    Returns:
        bool: True if normal operation can continue, False if the procedure needs to be halted.
    """
    try:
        app_logger.debug("Start check_and_reply_messages")
        if get_reply_data():
            time.sleep(1)
            make_reply()
            time.sleep(2)
            if check_risk_exit():
                time.sleep(1)
                make_risk_exit()
                time.sleep(1)
                set_is_running_grind_procedure(False)
                app_logger.debug("check_and_reply_messages() return False - grinder procedure need be stop")
                return False
            if check_risk_afk():
                time.sleep(1)
                make_risk_afk()
                time.sleep(1)
                app_logger.debug("check_risk_afk() return False - grinder procedure need be stop")
                return False
        app_logger.debug("check_and_reply_messages - return True")
        return True
    except Exception as ex:
        app_logger.error(ex)

def store_items_procedure():
    """
    Executes the procedure for storing items in the game.

    This function automates the in-game actions required to store collected items properly.
    """
    app_logger.info("Start stored items procedure")
    time.sleep(0.8)
    items_stored_procedure()
    time.sleep(0.8)

def grinder_procedure_loop() -> None:
    """
    Main loop for the grinder procedure.

    This function orchestrates the entire grinder procedure including teleporting, grinding, storing items,
    and sending notifications, in a loop as long as the procedure is active.
    """
    try:
        app_logger.debug("Starting grinder_procedure_loop")
        while get_is_running_grind_procedure():
            time.sleep(1)
            if not afk_break():
                tp_to_spawn()
            time.sleep(1)
            tp_to_mobgrinder_home()
            time.sleep(return_random_wait_interval_time(1, 3))
            if not grind_procedure():
                break
            store_items_procedure()
            send_chat_notification()
            restoring_incubator_procedure()
        app_logger.debug("grinder_procedure_loop() end while loop - not get_is_running_grind_procedure()")
    except Exception as ex:
        app_logger.error(ex)

def toggle_grinder_procedure() -> None:
    """
    Toggles the state of the grinder procedure.

    This function switches the grinder procedure on or off and manages the corresponding threading.
    It ensures that no other procedures like farming or mining are running concurrently.
    """
    try:
        global is_running_grind_procedure
        global grinder_procedure_thread
        from activities.farm import is_running_farm_procedure
        from activities.mine import is_running_mine_procedure
        if is_running_farm_procedure or is_running_mine_procedure:
            app_logger.info(f"Can not start farm procedure - other procedure is running")
        else:
            is_running_grind_procedure = not is_running_grind_procedure
            state = 'started' if is_running_grind_procedure else 'stopped'
            app_logger.info(f"MobGrinder procedure {state}")
            print(f"MobGrinder procedure {state}")
            if is_running_grind_procedure:
                if grinder_procedure_thread is None or not grinder_procedure_thread.is_alive():
                    grinder_procedure_thread = threading.Thread(target=grinder_procedure_loop)
                    grinder_procedure_thread.start()
    except Exception as ex:
        app_logger.error(ex)
