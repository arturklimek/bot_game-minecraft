import copy
import random
import threading
import time
import datetime
from typing import Optional
import keyboard
import mouse
import pyautogui
import activities.eq_bar
from activities.afk import afk_break, draw_risk_afk_time, afk_on_spawn
from activities.chat import tp_to_mining_home, send_on_chat, sellall_inventory, tp_to_chest_home, tp_to_spawn, \
    send_chat_notification, send_random_message_coordinates_problem
from activities.chest import check_and_get_chest_image, get_slots_chest_coordinates, get_chest_slots_images, \
    eq_slots_amount, eq_inventory_amount, find_item_pattern_in_item_image, calc_and_get_screenshoot_sloot_coordinates, \
    shift_click_at_coordinates_in_game_window, chest_inventory_elements
from activities.eq_bar import check_pickaxe_damage_to_repair, get_pickaxe_image, \
    get_item_slot_number, check_and_update_eq_coordinates
from activities.equipment import check_inventory_full, check_slot_free
from activities.repair import repair_item
from app_config import items_quantity_pattern, get_repair_mining_pickaxe_frequency, get_hotkey_inventory, \
    get_hotkey_moving_up, get_hotkey_moving_left, get_hotkey_moving_right, get_hotkeys_slots, get_protected_slots, \
    set_protected_slots, get_moving_time, get_moving_hold_shift, get_items_stored_list, \
    get_coordinates_screen_XYZ_analysis_flag, get_mine_coordinate_range
from clicker import click_right_mouse_button
from coordinate_analyzer import check_coordinates_compatibility_XYZ, get_coordinates_XYZ
from delay import return_random_wait_interval_time
from image_operations import convert_cv_image_to_gray, load_cv_image
from log_game_processor import get_reply_data, check_risk_exit, check_risk_afk, make_reply, make_risk_afk, \
    make_risk_exit
from logger import app_logger
from patterns import items_patterns
from screenshooter import get_last_screenshot

mine_procedure_thread = None
pickaxe_damage_checker_thread = None

is_running_mine_procedure = False

current_moving_direction = None
current_stops_count = 0
target_stops_count = 0
moving_flag = True
stored_flag = False
repair_flag = False
pickaxe_slot = 9

max_coordinates_without_moving = 3
max_coordinates_without_data = 5
max_coordinates_out_of_range = 3

# last_farm_time = None

def get_is_running_mine_procedure() -> bool:
    return is_running_mine_procedure

def set_is_running_mine_procedure(state: bool = False) -> None:
    global is_running_mine_procedure
    is_running_mine_procedure = state

def items_stored_procedure() -> None:
    """
    Handles the procedure for storing items in the chest and selling them.

    This function automates the process of teleporting to the chest home, interacting with the chest, identifying items to store, and performing actions like storing and selling items. It utilizes image recognition to find specific items in the inventory and interact with them accordingly.

    Note:
        The function is designed to work within a specific game environment, and its effectiveness is dependent on the accuracy of image pattern recognition.
    """
    try:
        tp_to_chest_home()
        app_logger.debug("items_stored_procedure use tp_to_chest_home()")
        time.sleep(return_random_wait_interval_time(0.4, 1))
        click_right_mouse_button()
        time.sleep(0.3)
        x = -(int(chest_inventory_elements["chest-big"]["width"] / 2))
        y = -(int(chest_inventory_elements["chest-big"]["height"] / 2))
        pyautogui.move(x, y)
        app_logger.debug(f"items_stored_procedure moved mouse to x: {x} y: {y}")
        time.sleep(1)
        chest = check_and_get_chest_image()
        if chest is not None:
            cropped_chest_image, chest_top_left, chest_bottom_right, chest_size = chest
            app_logger.debug(
                f"chest - chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right} chest_size: {chest_size}")
            slots_coordinates = get_slots_chest_coordinates(cropped_chest_image, chest_size)
            app_logger.debug(f"geted slots_coordinates: {slots_coordinates}")
            slots_images = get_chest_slots_images(cropped_chest_image, slots_coordinates)
            app_logger.debug(f"geted {len(slots_images)} slot images")
            item_quantity_mask = convert_cv_image_to_gray(load_cv_image(items_quantity_pattern))
            slots_coordinates_to_stored = []
            slots_amount = eq_slots_amount + eq_inventory_amount
            slots_images_to_analize = slots_images[0:slots_amount]
            app_logger.debug(f"slots_images_to_analize have {len(slots_images_to_analize)} elements.")
            slots_coordinates_to_analize = slots_coordinates[0:slots_amount]
            app_logger.debug(f"slots_coordinates_to_analize have {len(slots_coordinates_to_analize)} elements: {slots_coordinates_to_analize}")
            for i, slot in enumerate(slots_images_to_analize):
                if i >= slots_amount:
                    app_logger.debug(f"i: {i} is greater than or equal to eq_slots_amount + eq_inventory_amount: {slots_amount} - break")
                    break
                if i + 1 in get_protected_slots():
                    app_logger.debug(f"i: {i} +1 is in protected_slots - continue")
                    continue
                selected_item = find_item_pattern_in_item_image(slot, item_quantity_mask, items_patterns)
                app_logger.debug(f"selected_item: {selected_item}")
                app_logger.debug(f"get_items_stored_list(): {get_items_stored_list()}")
                if selected_item is not None:
                    if selected_item in get_items_stored_list():
                        slots_coordinates_to_stored.insert(i, slots_coordinates_to_analize[i])
            app_logger.debug(f"slots_coordinates_to_stored have {len(slots_coordinates_to_stored)} elements")
            screen_coordinates_to_click = []
            for slot_coordinates in slots_coordinates_to_stored:
                screen_coordinates_to_click.append(
                    calc_and_get_screenshoot_sloot_coordinates(slot_coordinates, chest_top_left, chest_bottom_right))
            for slot_to_click in screen_coordinates_to_click:
                shift_click_at_coordinates_in_game_window(slot_to_click)
            app_logger.debug(f"screen_coordinates_to_click have {len(screen_coordinates_to_click)} elements")
            time.sleep(return_random_wait_interval_time(0.1, 0.5))
            keyboard.press_and_release(get_hotkey_inventory())
            app_logger.debug(f"items_stored_procedure press and release: {get_hotkey_inventory()}")
            time.sleep(return_random_wait_interval_time(0.1, 0.5))
            sellall_inventory()
            time.sleep(return_random_wait_interval_time(0.1, 0.5))
            click_right_mouse_button()
            time.sleep(0.3)
            x = -(int(chest_inventory_elements["chest-big"]["width"] / 2))
            y = -(int(chest_inventory_elements["chest-big"]["height"] / 2))
            pyautogui.move(x, y)
            app_logger.debug(f"items_stored_procedure moved mouse to x: {x} y: {y}")
            time.sleep(1)
            chest = check_and_get_chest_image()
            if chest is not None:
                cropped_chest_image, chest_top_left, chest_bottom_right, chest_size = chest
                app_logger.debug(
                    f"chest - chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right} chest_size: {chest_size}")
                slots_coordinates = get_slots_chest_coordinates(cropped_chest_image, chest_size)
                app_logger.debug(f"slots_coordinates have {len(slots_coordinates)} elements: {slots_coordinates}")
                slots_images = get_chest_slots_images(cropped_chest_image, slots_coordinates)
                app_logger.debug(f"slots_images have {len(slots_images)} elements")
                slots_images_to_analize = slots_images[0:slots_amount]
                app_logger.debug(f"slots_images_to_analize have {len(slots_images_to_analize)} elements")
                slots_coordinates_to_analize = slots_coordinates[0:slots_amount]
                app_logger.debug(
                    f"slots_coordinates_to_analize have {len(slots_coordinates_to_analize)} elements: {slots_coordinates_to_analize}")
                screen_coordinates_to_click.clear()
                app_logger.debug(f"screen_coordinates_to_click was clear")
                for i, slot_image in enumerate(slots_images_to_analize):
                    if i >= slots_amount:
                        break
                    if i + 1 in get_protected_slots():
                        continue
                    if not check_slot_free(slot_image):
                        screen_coordinates_to_click.append(
                            calc_and_get_screenshoot_sloot_coordinates(slots_coordinates_to_analize[i], chest_top_left,
                                                                       chest_bottom_right))
                app_logger.debug(
                    f"screen_coordinates_to_click was upadted, now have {len(screen_coordinates_to_click)} elements: {screen_coordinates_to_click}")
                for slot_to_click in screen_coordinates_to_click:
                    shift_click_at_coordinates_in_game_window(slot_to_click)
            else:
                app_logger.debug(f"chest is None")
            time.sleep(0.3)
            keyboard.press_and_release(get_hotkey_inventory())
            app_logger.debug(f"items_stored_procedure press and release: {get_hotkey_inventory()}")
        else:
            app_logger.debug(f"chest taked from check_and_get_chest_image() is None")
    except Exception as ex:
        app_logger.error(ex)

def change_pickaxe_slot_number(pickaxe_top_left: Optional[tuple] = None, pickaxe_bottom_right: Optional[tuple] = None) -> None:
    """
    Updates the slot number of the pickaxe in the inventory.

    Args:
        pickaxe_top_left (tuple): The top left coordinates of the pickaxe image in the inventory.
        pickaxe_bottom_right (tuple): The bottom right coordinates of the pickaxe image in the inventory.

    This function identifies the new slot number of the pickaxe based on its position in the inventory and updates the global variable 'pickaxe_slot'. It also adjusts the set of protected slots accordingly.

    Note:
        If the coordinates are not provided, the function attempts to locate the pickaxe automatically.
    """
    global pickaxe_slot
    try:
        if pickaxe_top_left is None or pickaxe_bottom_right is None:
            app_logger.debug(f"pickaxe_top_left: {pickaxe_top_left} OR pickaxe_bottom_right: {pickaxe_bottom_right} is none - try get_pickaxe_image()")
            pickaxe = get_pickaxe_image()
            if pickaxe:
                image_pickaxe, pickaxe_top_left, pickaxe_bottom_right = pickaxe
                app_logger.debug(f"Taked pickaxe pickaxe_top_left: {pickaxe_top_left} pickaxe_bottom_right: {pickaxe_bottom_right}")
            else:
                app_logger.debug("Can not get pickaxe")
                return
        new_pickaxe_slot = get_item_slot_number(pickaxe_top_left, pickaxe_bottom_right)
        app_logger.debug(f"new_pickaxe_slot: {new_pickaxe_slot}")
        if new_pickaxe_slot != pickaxe_slot:
            protected_slots = set(get_protected_slots())
            app_logger.debug(f"protected_slots: {protected_slots}")
            if pickaxe_slot in protected_slots:
                protected_slots.remove(pickaxe_slot)
                app_logger.debug(f"pickaxe_slot: {pickaxe_slot} is in protected_slots - removing")
                app_logger.debug(f"protected_slots: {protected_slots}")
                set_protected_slots(protected_slots)
            if new_pickaxe_slot not in protected_slots:
                app_logger.debug(f"new_pickaxe_slot: {pickaxe_slot} is not in protected_slots - adding")
                app_logger.debug(f"protected_slots: {protected_slots}")
                protected_slots.add(new_pickaxe_slot)
                set_protected_slots(protected_slots)
            pickaxe_slot = new_pickaxe_slot
        else:
            app_logger.debug("new_pickaxe_slot and pickaxe_slot have that same value")
    except Exception as ex:
        app_logger.error(ex)

def off_drop(drop_name: str) -> None:
    """
    Sends a command to the game chat to turn off the drop of a specified item.

    Args:
        drop_name (str): The name of the item for which the drop is to be turned off.

    The function sends a specific command format to the game chat, which is recognized by the game to turn off the drop of the specified item.
    """
    send_on_chat(f"/wylaczdrop {drop_name}")
    app_logger.debug(f"off_drop() was used (command: /wylaczdrop {drop_name})")

def move_direction_and_mine() -> None:
    """
    Automates the mining process in a specified direction.

    This function handles the automated movement and mining activity in the game. It involves moving in the current direction, using the pickaxe, and handling various checks such as whether mining is still ongoing and if the direction needs to be changed.

    Note:
        The function is part of a larger automated mining procedure and relies on global variables to manage the state and direction of mining.
    """
    global moving_flag
    global current_moving_direction
    coordinate_analyze_flag = get_coordinates_screen_XYZ_analysis_flag()
    app_logger.debug("Starting move_direction")
    tmp_moving_time = random.randint(int(get_moving_time()*0.8),int(get_moving_time()*1.2))
    app_logger.debug(f"tmp_moving_time was draw to value: {tmp_moving_time}")
    if is_running_mine_procedure and current_moving_direction:
        keyboard.press_and_release(get_hotkeys_slots()[pickaxe_slot])
        app_logger.debug(f"Press and relase: {get_hotkeys_slots()[pickaxe_slot]} - pickaxe_slot: {pickaxe_slot}")
        press_mine_buttons()
        last_iteration_time = datetime.datetime.now()
        last_coordinates = {}
        coordinates_without_moving = 0
        coordinates_without_data = 0
        coordinates_out_of_range = 0
        for time_iteration in range(tmp_moving_time*2):
            if not is_running_mine_procedure:
                app_logger.debug(f"is_running_mine_procedure is {is_running_mine_procedure} - break")
                break
            if not moving_flag:
                app_logger.debug(f"moving_flag is {moving_flag} - break")
                break
            if get_reply_data():
                # remaining_time = tmp_moving_time*2 - time_iteration*0.5
                release_mine_buttons()
                time.sleep(1)
                make_reply()
                time.sleep(2)
                if check_risk_exit():
                    time.sleep(1)
                    make_risk_exit()
                    time.sleep(1)
                    set_is_running_mine_procedure(False)
                    # global is_running_mine_procedure
                    # is_running_mine_procedure = False
                    # toggle_mine_procedure()
                    return
                if check_risk_afk():
                    time.sleep(1)
                    make_risk_afk()
                    time.sleep(1)
                    current_moving_direction = get_hotkey_moving_right()
                    app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                    tp_to_mining_home()
                    return
                keyboard.press_and_release(get_hotkeys_slots()[pickaxe_slot])
                app_logger.debug(
                    f"Press and relase: {get_hotkeys_slots()[pickaxe_slot]} - pickaxe_slot: {pickaxe_slot}")
                press_mine_buttons()
            if coordinate_analyze_flag:
                current_time = datetime.datetime.now()
                time_difference = current_time - last_iteration_time
                if time_difference.total_seconds() < 1:
                    app_logger.debug("Less than 1 second has passed since the last iteration")
                else:
                    coordinates_range = get_mine_coordinate_range()
                    app_logger.debug(f"coordinates_range: {coordinates_range}")
                    current_coordinates = get_coordinates_XYZ()
                    coordinate_state = check_coordinates_compatibility_XYZ(coordinates_range, current_coordinates)
                    if coordinate_state is False:
                        coordinates_without_data = 0
                        coordinates_out_of_range = coordinates_out_of_range + 1
                        app_logger.debug(f"coordinate_state is {coordinate_state}, set coordinates_out_of_range to value: {coordinates_out_of_range}")
                        pass
                    elif coordinate_state is True:
                        coordinates_without_data = 0
                        coordinates_out_of_range = 0
                        app_logger.debug(f"coordinate_state is {coordinate_state} - SET coordinates_without_data: {coordinates_without_data} and coordinates_out_of_range: {coordinates_out_of_range}")
                        pass
                    else:
                        coordinates_without_data = coordinates_without_data + 1
                        app_logger.debug(f"coordinate_state is {coordinate_state} - set coordinates_without_data to value: {coordinates_without_data}")

                    if last_coordinates:
                        if last_coordinates == current_coordinates:
                            coordinates_without_moving = coordinates_without_moving + 1
                            app_logger.debug(f"coordinates do not change - set coordinates_without_moving to value: {coordinates_without_moving} last_coordinates: {last_coordinates} current_coordinates: {current_coordinates}")
                        else:
                            coordinates_without_moving = 0
                    if coordinates_without_moving > max_coordinates_without_moving:
                        app_logger.warning(f"coordinates_without_moving: {coordinates_without_moving} exceeded the max value: {max_coordinates_without_moving}")
                        release_mine_buttons()
                        random_double_move_mouse()
                        time.sleep(1)
                        send_random_message_coordinates_problem()
                        app_logger.info(f"Go to Lobby (too many coordinates without moving)")
                        go_lobby_exit_mine()
                        return
                    if coordinates_without_data > max_coordinates_without_data:
                        app_logger.warning(
                            f"coordinates_without_data: {coordinates_without_data} exceeded the max value: {max_coordinates_without_data}")
                        release_mine_buttons()
                        time.sleep(1)
                        send_random_message_coordinates_problem()
                        afk_time = draw_risk_afk_time()
                        app_logger.info(f"Go AFK on spawn (too many coordinates without data) for afk_time: {afk_time}")
                        afk_on_spawn(afk_time)
                        app_logger.debug("AFK time over")
                        time.sleep(1)
                        current_moving_direction = get_hotkey_moving_right()
                        app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                        tp_to_mining_home()
                        return
                    if coordinates_out_of_range > max_coordinates_out_of_range:
                        app_logger.warning(
                            f"coordinates_out_of_range: {coordinates_out_of_range} exceeded the max value: {max_coordinates_out_of_range}")
                        release_mine_buttons()
                        random_double_move_mouse()
                        time.sleep(1)
                        send_random_message_coordinates_problem()
                        app_logger.info(f"Go to Lobby (too many coordinates out of range)")
                        go_lobby_exit_mine()
                        return
                    last_coordinates = current_coordinates
                    last_iteration_time = current_time
            time.sleep(0.5)
        release_mine_buttons()
        if is_running_mine_procedure:
            if current_moving_direction == get_hotkey_moving_right():
                current_moving_direction = get_hotkey_moving_left()
                app_logger.debug(f"Change current_moving_direction to hotkey_moving_left: {get_hotkey_moving_left()}")
            elif current_moving_direction == get_hotkey_moving_left():
                current_moving_direction = get_hotkey_moving_right()
                app_logger.debug(f"Change current_moving_direction to hotkey_moving_right: {get_hotkey_moving_right()}")
        else:
            app_logger.debug(f"is_running_mine_procedure is: {is_running_mine_procedure}")

def release_mine_buttons() -> None:
    """
    Releases the keys and mouse buttons used for mining.

    This function releases the 'left' mouse button and, if configured, the 'shift' key.
    It also releases the current movement direction key being pressed.
    It's typically used to stop the mining action in the game.
    """
    app_logger.debug(f"Release 'left'")
    pyautogui.mouseUp(button='left')
    if get_moving_hold_shift():
        app_logger.debug(f"Release 'shift'")
        keyboard.release('shift')
    app_logger.debug(f"Release {current_moving_direction}")
    keyboard.release(current_moving_direction)

def press_mine_buttons() -> None:
    """
    Presses the keys and mouse buttons required for mining.

    This function presses the current movement direction key, the 'left' mouse button for mining,
    and, if configured, holds the 'shift' key.
    It's used to initiate or continue the mining action in the game.
    """
    app_logger.debug(f"Pressing {current_moving_direction}")
    keyboard.press(current_moving_direction)
    if get_moving_hold_shift():
        app_logger.debug(f"Pressing 'shift'")
        keyboard.press('shift')
    app_logger.debug(f"Pressing 'left'")
    pyautogui.mouseDown(button='left')

def random_double_move_mouse() -> None:
    """
    Performs a random double movement of the mouse.

    This function randomly moves the mouse in the x and y directions and then back.
    It simulates natural mouse movement during gaming, particularly useful in scenarios like mining in Minecraft.
    """
    x_mouse_move = random.randint(20, 50)
    y_mouse_move = random.randint(0, 5)
    app_logger.debug(f"x: {x_mouse_move} y: {y_mouse_move}")
    mouse.move(x_mouse_move * random.choice([-1, 1]), y_mouse_move, absolute=False, duration=1)
    time_sleep = random.uniform(0.5, 2)
    app_logger.debug(f"time_sleep: {time_sleep}")
    time.sleep(time_sleep)
    mouse.move(x_mouse_move * random.choice([-1, 1]), 0, absolute=False, duration=1)

def go_lobby_exit_mine() -> None:
    """
    Sends the player to the lobby and stops the mining procedure.

    This function sends a command to the game chat to teleport the player to the game's lobby.
    It also sets the flag to stop the mining procedure.
    """
    lobby_command = "/lobby 1"
    time.sleep(1)
    app_logger.info(f"Go to Lobby - execute command: {lobby_command}")
    send_on_chat(lobby_command)
    time.sleep(5)
    set_is_running_mine_procedure(False)

def pickaxe_damage_checker() -> None:
    """
    Continuously checks the damage level of the pickaxe during mining.

    This function runs in a separate thread and periodically checks if the pickaxe is damaged and needs repair. If repair is needed, it automates the process of repairing the pickaxe, including teleporting to the repair location and interacting with the game environment.

    Note:
        This function is a critical component of the automated mining system, ensuring the pickaxe remains functional throughout the mining process.
    """
    global moving_flag
    global stored_flag
    global repair_flag
    app_logger.debug("Starting pickaxe_damage_checker()")
    while is_running_mine_procedure:
        try:
            app_logger.debug(f"pickaxe_damage_checker start sleep for {get_repair_mining_pickaxe_frequency()} seconds")
            time.sleep(get_repair_mining_pickaxe_frequency())
            if stored_flag:
                app_logger.debug(f"stored_flag is {stored_flag}")
                continue
            last_image = copy.copy(get_last_screenshot())
            eq_slot_x1, eq_slot_y1 = activities.eq_bar.eq_slot_top_left
            eq_slot_x2, eq_slot_y2 = activities.eq_bar.eq_slot_bottom_right
            cropped_slots_image = last_image[eq_slot_y1:eq_slot_y2, eq_slot_x1:eq_slot_x2]
            # cropped_pickaxe_image, pickaxe_top_left, pickaxe_bottom_right = get_pickaxe_image(cropped_slots_image)
            pickaxe_image_result = get_pickaxe_image(cropped_slots_image)
            if pickaxe_image_result is not None:
                cropped_pickaxe_image, pickaxe_top_left, pickaxe_bottom_right = pickaxe_image_result
                app_logger.debug(f"pickaxe_image_result - pickaxe_top_left: {pickaxe_top_left} pickaxe_bottom_right: {pickaxe_bottom_right}")
                change_pickaxe_slot_number(pickaxe_top_left, pickaxe_bottom_right)
                pickaxe_repair_status = check_pickaxe_damage_to_repair(cropped_pickaxe_image)
                app_logger.debug(f"pickaxe_repair_status is {pickaxe_repair_status}")
                if pickaxe_repair_status:
                    moving_flag = False
                    app_logger.debug(f"moving_flag set to {moving_flag}")
                    repair_flag = True
                    app_logger.debug(f"repair_flag set to {repair_flag}")
                    time.sleep(return_random_wait_interval_time(1, 1.5))
                    check_and_update_eq_coordinates()
                    time.sleep(return_random_wait_interval_time(0.1, 0.5))
                    change_pickaxe_slot_number(pickaxe_top_left, pickaxe_bottom_right)
                    time.sleep(return_random_wait_interval_time(0.1, 0.75))
                    repair_item()
                    time.sleep(return_random_wait_interval_time(0.1, 0.75))
                    global current_moving_direction
                    current_moving_direction = get_hotkey_moving_right()
                    app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                    tp_to_mining_home()
                    keyboard.press(get_hotkey_moving_up())
                    app_logger.debug(f"Pressing {get_hotkey_moving_up()}")
                    time.sleep(0.5)
                    keyboard.release(get_hotkey_moving_up())
                    app_logger.debug(f"Release {get_hotkey_moving_up()}")
                    repair_flag = False
                    app_logger.debug(f"repair_flag set to: {repair_flag}")
                    moving_flag = True
                    app_logger.debug(f"moving_flag set to: {moving_flag}")
            else:
                app_logger.debug("pickaxe_image_result is None")
            #     moving_flag = False
            #     time.sleep(1)
            #     check_and_update_eq_coordinates()
            #     time.sleep(return_random_wait_interval_time(0.1, 0.5))
            #     change_pickaxe_slot_number(pickaxe_top_left, pickaxe_bottom_right)
        except Exception as ex:
            app_logger.warning(ex)

def mine_procedure() -> None:
    """
    Main function to start and manage the automated mining procedure.

    This function controls the overall mining process, including checking the inventory, managing item storage, handling equipment repair, and executing the mining loop. It also handles specific game-related commands and interactions.

    Note:
        This function coordinates various sub-tasks and relies on multiple global flags to control the flow and state of the mining process.
    """
    global is_running_mine_procedure
    global moving_flag
    global current_moving_direction
    global stored_flag
    global repair_flag
    app_logger.debug(f"mine_procedure is starting")
    current_moving_direction = get_hotkey_moving_right()
    app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
    time.sleep(return_random_wait_interval_time(0.25,1))
    off_drop("cobblestone")
    time.sleep(return_random_wait_interval_time(0.25,1))
    tp_to_mining_home()
    keyboard.press(get_hotkey_moving_up())
    time.sleep(0.5)
    keyboard.release(get_hotkey_moving_up())
    keyboard.press("shift")
    time.sleep(0.5)
    keyboard.release("shift")
    time.sleep(return_random_wait_interval_time(0.25,1))
    check_and_update_eq_coordinates()
    change_pickaxe_slot_number()
    time.sleep(return_random_wait_interval_time(0.25, 1))
    eq_check_counter = 3
    app_logger.debug(f"eq_check_counter was set to {eq_check_counter}")
    while is_running_mine_procedure:
        send_chat_notification()
        if moving_flag:
            if repair_flag:
                app_logger.debug(f"repair_flag is {repair_flag} - continue")
                continue
            move_direction_and_mine()
            keyboard.press(get_hotkey_moving_up())
            time.sleep(0.2)
            keyboard.release(get_hotkey_moving_up())
            time.sleep(0.1)
            eq_check_counter = eq_check_counter - 1
            app_logger.debug(f"eq_check_counter was set to {eq_check_counter}")
            if eq_check_counter <= 0:
                app_logger.debug(f"eq_check_counter jet less than or equal to 0")
                eq_check_counter = random.randint(2,4)
                app_logger.debug(f"eq_check_counter was set to {eq_check_counter}")
                inventory_status = check_inventory_full()
                app_logger.debug(f"inventory_status is {inventory_status}")
                if inventory_status:
                    stored_flag = True
                    app_logger.debug(f"stored_flag was set to {stored_flag}")
                    time.sleep(0.8)
                    app_logger.info("EQ inventory is full. Start stored procedure")
                    items_stored_procedure()
                    # time.sleep(0.8)
                    # if farm_toggle:
                    #     global last_farm_time
                    #     current_time = datetime.now()
                    #     if last_farm_time is None or current_time - last_farm_time >= timedelta(minutes=farm_frequency):
                    #         last_farm_time = current_time
                    #         from activities.farm import farm_procedure
                    #         farm_procedure()
                    time.sleep(0.8)
                    current_moving_direction = get_hotkey_moving_right()
                    app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                    tp_to_spawn()
                    time.sleep(1)
                    tp_to_mining_home()
                    time.sleep(0.8)
                    stored_flag = False
                    app_logger.debug(f"stored_flag was set to {stored_flag}")
            if afk_break():
                current_moving_direction = get_hotkey_moving_right()
                app_logger.debug(f"current_moving_direction was set to: {current_moving_direction}")
                tp_to_mining_home()
                time.sleep(1)
        time.sleep(return_random_wait_interval_time())

def toggle_mine_procedure() -> None:
    """
    Toggles the state of the mining procedure, starting or stopping it.

    This function is used to start or stop the automated mining procedure. It initializes or terminates the mining and pickaxe damage checking threads based on the current state. It also ensures that mining does not start if another procedure is running.

    Note:
        This function acts as a switch to control the execution of the automated mining procedure.
    """
    global is_running_mine_procedure
    global mine_procedure_thread
    global pickaxe_damage_checker_thread
    from activities.farm import is_running_farm_procedure
    if is_running_farm_procedure:
        app_logger.info(f"Can not start mining procedure - other procedure is running")
    else:
        is_running_mine_procedure = not is_running_mine_procedure
        state = 'started' if is_running_mine_procedure else 'stopped'
        app_logger.info(f"Mining procedure {state}")
        if is_running_mine_procedure:
            if mine_procedure_thread is None or not mine_procedure_thread.is_alive():
                mine_procedure_thread = threading.Thread(target=mine_procedure)
                mine_procedure_thread.start()
            if pickaxe_damage_checker_thread is None or not pickaxe_damage_checker_thread.is_alive():
                pickaxe_damage_checker_thread = threading.Thread(target=pickaxe_damage_checker)
                pickaxe_damage_checker_thread.start()
