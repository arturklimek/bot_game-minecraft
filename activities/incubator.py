import time
from datetime import datetime, timedelta
from typing import Optional, Tuple
import keyboard
import pyautogui
from activities.chat import send_incubator_reset_command, send_incubator_command
from activities.chest import check_and_get_chest_image, get_chest_inventory_elements, get_slots_chest_coordinates, \
    get_chest_slots_images, get_eq_inventory_amount, get_eq_slots_amount, find_item_pattern_in_item_image, \
    calc_and_get_screenshoot_sloot_coordinates, shift_click_at_coordinates_in_game_window
from activities.eq_bar import get_item_slot_number, get_obscure_matter_image
from app_config import get_hotkeys_slots, items_quantity_pattern, get_incubator_list, get_hotkey_inventory, \
    get_incubator_restore
from delay import return_random_wait_interval_time
from image_operations import convert_cv_image_to_gray, load_cv_image, save_image_for_function
from logger import app_logger

obscure_matter_slot = 8

def get_obscure_matter_slot() -> int:
    return obscure_matter_slot

last_incubator_reset_time = datetime.now()

def get_last_incubator_reset_time() :
    return last_incubator_reset_time

def set_last_incubator_reset_time(new_time):
    global last_incubator_reset_time
    last_incubator_reset_time = new_time

def set_obscure_matter_slot(new_slot_number: int = 8):
    global obscure_matter_slot
    obscure_matter_slot = new_slot_number

def incubator_reset() -> None:
    """
    Executes the incubator reset process.
    """
    try:
        app_logger.debug("Start incubator_reset()")
        time.sleep(0.5)
        change_incubator_slot_number()
        time.sleep(0.3)
        app_logger.debug(f"Press and release {get_hotkeys_slots()[get_obscure_matter_slot()]}")
        keyboard.press_and_release(get_hotkeys_slots()[get_obscure_matter_slot()])
        time.sleep(0.3)
        send_incubator_reset_command()
        time.sleep(0.5)
    except Exception as ex:
        app_logger.error(ex)

def incubators_activation() -> None:
    """
    Activates the incubators.
    """
    try:
        app_logger.debug("Start incubators_activation()")
        send_incubator_command()
        x = -(int(get_chest_inventory_elements()["chest-big"]["width"] / 2))
        y = -(int(get_chest_inventory_elements()["chest-big"]["height"] / 2))
        pyautogui.move(x, y, 0.3)
        app_logger.debug(f"incubators_activation moved mouse to x: {x} y: {y}")
        time.sleep(2)
        chest = check_and_get_chest_image()
        if chest is not None:
            cropped_chest_image, chest_top_left, chest_bottom_right, chest_size = chest
            app_logger.debug(
                f"chest - chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right} chest_size: {chest_size}")
            save_image_for_function("incubators_activation", "cropped_chest_image", cropped_chest_image)
            slots_coordinates = get_slots_chest_coordinates(cropped_chest_image, chest_size)
            app_logger.debug(f"geted slots_coordinates: {slots_coordinates}")
            slots_images = get_chest_slots_images(cropped_chest_image, slots_coordinates)
            app_logger.debug(f"geted {len(slots_images)} slot images")
            item_quantity_mask = convert_cv_image_to_gray(load_cv_image(items_quantity_pattern))
            slots_coordinates_to_stored = []
            slots_amount = get_eq_slots_amount() + get_eq_inventory_amount()
            slots_images_to_analize = slots_images[slots_amount:]
            app_logger.debug(f"slots_images_to_analize have {len(slots_images_to_analize)} elements.")
            slots_coordinates_to_analize = slots_coordinates[slots_amount:]
            app_logger.debug(f"slots_coordinates_to_analize have {len(slots_coordinates_to_analize)} elements: {slots_coordinates_to_analize}")
            for i, slot in enumerate(slots_images_to_analize):
                selected_item = find_item_pattern_in_item_image(slot, item_quantity_mask)
                save_image_for_function("incubators_activation", "slot", slot)
                app_logger.debug(f"selected_item: {selected_item}")
                app_logger.debug(f"get_items_stored_list(): {get_incubator_list()}")
                if selected_item is not None:
                    if selected_item in get_incubator_list():
                        slots_coordinates_to_stored.insert(i, slots_coordinates_to_analize[i])
            app_logger.debug(f"slots_coordinates_to_stored have {len(slots_coordinates_to_stored)} elements")
            screen_coordinates_to_click = []
            for slot_coordinates in slots_coordinates_to_stored:
                screen_coordinates_to_click.append(
                    calc_and_get_screenshoot_sloot_coordinates(slot_coordinates, chest_top_left, chest_bottom_right))
            app_logger.debug(f"screen_coordinates_to_click have {len(screen_coordinates_to_click)} elements")
            for slot_to_click in screen_coordinates_to_click:
                shift_click_at_coordinates_in_game_window(slot_to_click)
            time.sleep(return_random_wait_interval_time(0.1, 0.5))
        else:
            app_logger.debug(f"chest taked from check_and_get_chest_image() is None")
        app_logger.debug(f"incubators_activation press and release: {get_hotkey_inventory()}")
        keyboard.press_and_release(get_hotkey_inventory())
        time.sleep(return_random_wait_interval_time(0.1, 0.5))
    except Exception as ex:
        app_logger.error(ex)

def restoring_incubator_procedure() -> None:
    """
    Executes the procedure for restoring the incubator if certain conditions are met.
    """
    try:
        app_logger.debug(f"Start restoring_incubator_procedure()")
        current_time = datetime.now()
        if get_incubator_restore() > 0 and current_time - get_last_incubator_reset_time() >= timedelta(minutes=get_incubator_restore()):
            time.sleep(return_random_wait_interval_time(0.25, 1))
            incubator_reset()
            incubators_activation()
            time.sleep(return_random_wait_interval_time(0.25, 0.5))
            set_last_incubator_reset_time(current_time)
        else:
            app_logger.debug(f"Incubator reset time condition not met")
    except Exception as ex:
        app_logger.error(ex)

def change_incubator_slot_number(obscure_matter_top_left: Optional[Tuple[int, int]] = None, obscure_matter_bottom_right: Optional[Tuple[int, int]] = None) -> None:
    """
    Changes the slot number of the incubator based on the position of the obscure matter.

    Args:
        obscure_matter_top_left (Optional[Tuple[int, int]]): Top left coordinates of the obscure matter.
        obscure_matter_bottom_right (Optional[Tuple[int, int]]): Bottom right coordinates of the obscure matter.
    """
    try:
        app_logger.debug("Start change_incubator_slot_number")
        if obscure_matter_top_left is None or obscure_matter_bottom_right is None:
            keyboard.press_and_release(get_hotkeys_slots()[9])
            time.sleep(1)
            app_logger.debug(
                f"obscure_matter_top_left: {obscure_matter_top_left} OR obscure_matter_right: {obscure_matter_bottom_right} is None - try get_obscure_matter_image()")
            obscure_matter = get_obscure_matter_image()
            if obscure_matter:
                image_obscure_matter, obscure_matter_top_left, obscure_matter_bottom_right = obscure_matter
                app_logger.debug(f"obscure_matter_top_left: {obscure_matter_top_left} obscure_matter_bottom_right: {obscure_matter_bottom_right}")
            else:
                app_logger.debug(f"Taked obscure_matter is: {obscure_matter}")
                return
        new_obscure_matter_slot = get_item_slot_number(obscure_matter_top_left, obscure_matter_bottom_right)
        app_logger.debug(f"new_obscure_matter_slot is {new_obscure_matter_slot}")
        if new_obscure_matter_slot != get_obscure_matter_slot():
            app_logger.debug(f"obscure_matter_slot: {get_obscure_matter_slot()} changing to new_obscure_matter_slot: {new_obscure_matter_slot}")
            set_obscure_matter_slot(new_obscure_matter_slot)
        else:
            app_logger.debug("obscure_matter_slot and new_obscure_matter_slot are that same")
    except Exception as ex:
        app_logger.error(ex)
