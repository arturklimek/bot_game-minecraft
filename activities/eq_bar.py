import copy
import time
import cv2
import keyboard
from activities.item import analyze_damage_level
from app_config import get_repair_threshold, get_hotkeys_slots
from delay import return_random_wait_interval_time
from patterns import slots_patterns, pickaxe_patterns, axe_patterns
from image_operations import convert_cv_image_to_gray
from logger import app_logger
from screenshooter import get_last_screenshot, get_screenshot

eq_slot_top_left = None
eq_slot_bottom_right = None

def find_pickaxe_pattern(image, threshold=0.935): #TODO: przenieść część wspólną do jednej osobnej funkcji razem z find_eq_slots_pattern
    """
    Finds the pickaxe pattern in a given image using template matching.

    Args:
        image: The image to search for the pickaxe pattern.
        threshold: The threshold value for template matching, default is 0.935.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found pickaxe pattern, or None if not found.
    """
    app_logger.debug("find_pickaxe_pattern was used")
    app_logger.debug(f"used threshold: {threshold}")
    try:
        image_gray = convert_cv_image_to_gray(image)
        result = cv2.matchTemplate(image_gray, pickaxe_patterns["pickaxe_pattern"], cv2.TM_CCORR_NORMED, mask=pickaxe_patterns["pickaxe_pattern_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f"pickaxe max_val: {max_val} max_loc: {max_loc}")
        if max_val > threshold:
            top_left = max_loc
            w, h = pickaxe_patterns["pickaxe_pattern"].shape[1], pickaxe_patterns["pickaxe_pattern"].shape[0]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            app_logger.debug(f'pickaxe was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('pickaxe pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)


def find_eq_slots_pattern(image, threshold=0.9): # requires a slot set to 9
    """
    Finds the equipment slots pattern in a given image using template matching.

    Args:
        image: The image to search for the equipment slots pattern.
        threshold: The threshold value for template matching, default is 0.9.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found equipment slots pattern, or None if not found.
    """
    app_logger.debug("find_eq_slots_pattern was used")
    app_logger.debug(f"used threshold: {threshold}")
    try:
        image_gray = convert_cv_image_to_gray(image)
        result = cv2.matchTemplate(image_gray, slots_patterns["slots_pattern"], cv2.TM_CCORR_NORMED, mask=slots_patterns["slots_pattern_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f"pickaxe max_val: {max_val} max_loc: {max_loc}")
        if max_val > threshold:
            top_left = max_loc
            w, h = slots_patterns["slots_pattern"].shape[1], slots_patterns["slots_pattern"].shape[0]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            app_logger.debug(f'eq-slots was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('eq-slots pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)

def get_slots_image(image_screenshoot=None):
    """
    Retrieves the image of the equipment slots.

    Args:
        image_screenshoot: An optional screenshot image. If not provided, the function will take a new screenshot.

    Returns:
        A tuple containing the cropped slots image, top-left, and bottom-right coordinates of the slots, or None if not found.
    """
    app_logger.debug("get_slots_image was used")
    if image_screenshoot is None:
        app_logger.debug("image_screenshoot is None - try get_last_screenshot()")
        image = copy.copy(get_last_screenshot())
    else:
        image = copy.copy(image_screenshoot)
    try:
        eq_slot = find_eq_slots_pattern(image)
        if eq_slot is not None:
            eq_slot_top_left, eq_slot_bottom_right = eq_slot
            eq_slot_x1, eq_slot_y1 = eq_slot_top_left
            eq_slot_x2, eq_slot_y2 = eq_slot_bottom_right
            cropped_slots_image = image[eq_slot_y1:eq_slot_y2, eq_slot_x1:eq_slot_x2]
            return cropped_slots_image, eq_slot_top_left, eq_slot_bottom_right
        else:
            app_logger.debug("eq_slot is None")
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_item_slot_number(item_top_left=None, item_bottom_right=None):
    """
    Calculates the slot number of an item based on its position in the equipment inventory.

    Args:
        item_top_left: The top-left coordinate of the item.
        item_bottom_right: The bottom-right coordinate of the item.

    Returns:
        The slot number of the item, or None if coordinates are incorrect or an error occurs.
    """
    app_logger.debug("get_item_slot_number was used")
    try:
        if item_top_left is None or item_bottom_right is None:
            app_logger.warning(f"item_top_left or item_bottom_right is None in get_item_slot_number()")
            return None
        if item_top_left and item_bottom_right:
            item_x1, item_y1 = item_top_left
            item_x2, item_y2 = item_bottom_right
        else:
            app_logger.warning("Incorrect pickaxe coordinates")
            return None

        slots_width, slots_height = slots_patterns["slots_pattern"].shape[1], slots_patterns["slots_pattern"].shape[
            0]
        slot_size = int(slots_width / 9)
        app_logger.debug(f"slot_size: {slot_size}")
        item_slot_number = round(item_x1 / slot_size + 1)
        app_logger.debug(f"item_slot_number: {item_slot_number}")
        return item_slot_number
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_pickaxe_image(image_slots=None):  #TODO: przenieść część wspólną do jednej osobnej funkcji razem z get_axe_image
    """
    Retrieves the image of the pickaxe from the equipment slots.

    Args:
        image_slots: An optional image of the equipment slots.

    Returns:
        A tuple containing the cropped pickaxe image, top-left, and bottom-right coordinates of the pickaxe, or None if not found.
    """
    app_logger.debug("get_pickaxe_image was used")
    if image_slots is None:
        app_logger.debug("image_slots is None - try get_slots_image(get_last_screenshot())")
        image_slots, eq_slot_top_left, eq_slot_bottom_right = get_slots_image(get_last_screenshot())
        image = copy.copy(image_slots)
    else:
        image = copy.copy(image_slots)
    try:
        cropped_pickaxe_image = None
        pickaxe = find_pickaxe_pattern(image)
        if pickaxe is not None:
            pickaxe_top_left, pickaxe_bottom_right = pickaxe
            if pickaxe_top_left and pickaxe_bottom_right:
                pickaxe_x1, pickaxe_y1 = pickaxe_top_left
                pickaxe_x2, pickaxe_y2 = pickaxe_bottom_right
                cropped_pickaxe_image = image[pickaxe_y1:pickaxe_y2, pickaxe_x1:pickaxe_x2]
            return cropped_pickaxe_image, pickaxe_top_left, pickaxe_bottom_right
        else:
            app_logger.debug("pickaxe is None")
    except Exception as ex:
        app_logger.error(ex)
        return None

def check_pickaxe_damage_to_repair(image_pickaxe=None):
    """
    Checks if the pickaxe needs repair based on its damage level.

    Args:
        image_pickaxe: An optional image of the pickaxe.

    Returns:
        True if the pickaxe needs repair, False otherwise, or None if an error occurs.
    """
    app_logger.debug("check_pickaxe_damage_to_repair was used")
    if image_pickaxe is None:
        app_logger.debug("image_pickaxe is None - try get_pickaxe_image()")
        image_pickaxe, pickaxe_top_left, pickaxe_bottom_right = copy.copy(get_pickaxe_image())
        if not image_pickaxe:
            app_logger.debug("Taked image_pickaxe again is None - return")
            return None
    item_damage_id = analyze_damage_level(image_pickaxe)
    app_logger.info(f"check_pickaxe_damage_to_repair - item_damage_id: {item_damage_id}")
    if item_damage_id <= get_repair_threshold():
        app_logger.info(f"check_pickaxe_damage_to_repair: True")
        return True
    else:
        app_logger.info(f"check_pickaxe_damage_to_repair: False")
        return False

def find_axe_pattern(image, threshold=0.95):
    """
    Finds the axe pattern in a given image using template matching.

    Args:
        image: The image to search for the axe pattern.
        threshold: The threshold value for template matching, default is 0.95.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found axe pattern, or None if not found.
    """
    app_logger.debug("find_axe_pattern was used")
    app_logger.debug(f"used threshold: {threshold}")
    try:
        image_gray = convert_cv_image_to_gray(image)
        result = cv2.matchTemplate(image_gray, axe_patterns["axe_pattern"], cv2.TM_CCORR_NORMED, mask=axe_patterns["axe_pattern_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f"axe max_val: {max_val} max_loc:{max_loc}")
        if max_val > threshold:
            top_left = max_loc
            w, h = axe_patterns["axe_pattern"].shape[1], axe_patterns["axe_pattern"].shape[0]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            app_logger.debug(f'axe was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('axe pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)

def get_axe_image(image_slots=None):
    """
    Retrieves the image of the axe from the equipment slots.

    Args:
        image_slots: An optional image of the equipment slots.

    Returns:
        A tuple containing the cropped axe image, top-left, and bottom-right coordinates of the axe, or None if not found.
    """
    app_logger.debug("get_axe_image was used")
    if image_slots is None:
        app_logger.debug("image_slots is None - try get_slots_image(get_last_screenshot())")
        image_slots, eq_slot_top_left, eq_slot_bottom_right = get_slots_image(get_last_screenshot())
        image = copy.copy(image_slots)
    else:
        image = copy.copy(image_slots)
    try:
        cropped_axe_image = None
        axe = find_axe_pattern(image)
        if axe is not None:
            axe_top_left, axe_bottom_right = axe
            if axe_top_left and axe_bottom_right:
                axe_x1, axe_y1 = axe_top_left
                axe_x2, axe_y2 = axe_bottom_right
                cropped_axe_image = image[axe_y1:axe_y2, axe_x1:axe_x2]
            return cropped_axe_image, axe_top_left, axe_bottom_right
        else:
            app_logger.debug("axe is None")
    except Exception as ex:
        app_logger.error(ex)
        return None

def check_axe_damage_to_repair(image_axe=None):
    """
    Checks if the axe needs repair based on its damage level.

    Args:
        image_axe: An optional image of the axe.

    Returns:
        True if the axe needs repair, False otherwise, or None if an error occurs.
    """
    app_logger.debug("check_axe_damage_to_repair was used")
    if image_axe is None:
        app_logger.debug("image_axe is None - try get_axe_image()")
        image_axe, axe_top_left, axe_bottom_right = copy.copy(get_axe_image())
        if not image_axe:
            return None
    item_damage_id = analyze_damage_level(image_axe)
    app_logger.debug(f"check_axe_damage_to_repair - item_damage_id: {item_damage_id}")
    if item_damage_id <= get_repair_threshold():
        app_logger.info(f"check_axe_damage_to_repair: True")
        return True
    else:
        app_logger.info(f"check_axe_damage_to_repair: False")
        return False

def check_and_update_eq_coordinates():
    """
    Checks and updates the global coordinates of the equipment slots.

    This function captures a new screenshot, finds the equipment slots pattern, and updates the global coordinates.
    """
    app_logger.debug("check_and_update_eq_coordinates was used")
    global eq_slot_top_left
    global eq_slot_bottom_right
    try:
        time.sleep(return_random_wait_interval_time())
        keyboard.press_and_release(get_hotkeys_slots()[9])
        app_logger.debug(f"press and release: {get_hotkeys_slots()[9]}")
        time.sleep(return_random_wait_interval_time(0.2,0.6))
        new_screenshoot = get_screenshot()
        image_slots, eq_slot_top_left, eq_slot_bottom_right = get_slots_image(new_screenshoot)
        app_logger.debug(f"eq_slot_top_left was set to {eq_slot_top_left} eq_slot_bottom_right was set to {eq_slot_bottom_right}")
        time.sleep(return_random_wait_interval_time())
    except Exception as ex:
        app_logger.warning(ex)
