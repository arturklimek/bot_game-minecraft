import copy
import time
from typing import Tuple, Optional, Callable
import cv2
import keyboard
import numpy as np
from activities.item import analyze_damage_level
from app_config import get_repair_threshold, get_hotkeys_slots
from delay import return_random_wait_interval_time
from patterns import slots_patterns, pickaxe_patterns, axe_patterns, sword_patterns, obscure_matter_patterns, \
    obscure_matters_patterns
from image_operations import convert_cv_image_to_gray, save_image_for_function
from logger import app_logger
from screenshooter import get_last_screenshot, get_screenshot

eq_slot_top_left = None
eq_slot_bottom_right = None

def get_eq_slot_top_left():
    return eq_slot_top_left

def get_eq_slot_bottom_right():
    return eq_slot_bottom_right

def find_eq_slots_pattern(image: np.ndarray, threshold: float = 0.9) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: # requires a slot set to 9
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
        app_logger.debug(f"eq_slots max_val: {max_val} max_loc: {max_loc}")
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

def get_slots_image(image_screenshoot: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
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

def check_and_update_eq_coordinates() -> None:
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

def get_item_slot_number(item_top_left: Optional[Tuple[int, int]] = None, item_bottom_right: Optional[Tuple[int, int]] = None) -> Optional[int]:
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
        # item_slot_number = round(item_x1 / slot_size + 1)
        item_slot_number = (item_x1 // slot_size) + 1
        app_logger.debug(f"item_slot_number: {item_slot_number}")
        return item_slot_number
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_item_image(image_slots: Optional[np.ndarray], find_item_pattern: Callable) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    """
    Retrieves the image of an item from the equipment slots.

    Args:
        image_slots: An optional image of the equipment slots.
        find_item_pattern: Function to find the specific item pattern in the image.

    Returns:
        A tuple containing the cropped item image, top-left, and bottom-right coordinates of the item, or None if not found.
    """
    global eq_slot_top_left
    global eq_slot_bottom_right
    app_logger.debug("get_item_image was used")
    if image_slots is None:
        app_logger.debug("image_slots is None - try get_slots_image(get_last_screenshot())")
        image_slots, eq_slot_top_left, eq_slot_bottom_right = get_slots_image(get_last_screenshot())
        image = copy.copy(image_slots)
    else:
        image = copy.copy(image_slots)
    try:
        item = find_item_pattern(image)
        if item is not None:
            item_top_left, item_bottom_right = item
            if item_top_left and item_bottom_right:
                item_x1, item_y1 = item_top_left
                item_x2, item_y2 = item_bottom_right
                cropped_item_image = image[item_y1:item_y2, item_x1:item_x2]
                save_image_for_function("get_item_image", "cropped_item_image", cropped_item_image)
                return cropped_item_image, item_top_left, item_bottom_right
        else:
            app_logger.debug("Item is None")
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_pickaxe_image(image_slots: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    return get_item_image(image_slots, find_pickaxe_pattern)

def get_axe_image(image_slots: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    return get_item_image(image_slots, find_axe_pattern)

def get_sword_image(image_slots: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    return get_item_image(image_slots, find_sword_pattern)

def get_obscure_matter_image(image_slots: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    return get_item_image(image_slots, find_obscure_matter_pattern)

def check_item_damage_to_repair(item_image: Optional[np.ndarray], get_item_image_function) -> Optional[bool]:
    """
    Checks if an item needs repair based on its damage level.

    Args:
        item_image: An optional image of the item.
        get_item_image_function: A function to get the item's image if not provided.

    Returns:
        True if the item needs repair, False otherwise, or None if an error occurs.
    """
    app_logger.debug("check_item_damage_to_repair was used")
    if item_image is None:
        app_logger.debug("item_image is None - try get_item_image()")
        item_image, item_top_left, item_bottom_right = copy.copy(get_item_image_function())
        if not item_image:
            app_logger.debug("Taken item_image is None - return")
            return None
    item_damage_id = analyze_damage_level(item_image)
    app_logger.info(f"check_item_damage_to_repair - item_damage_id: {item_damage_id}")
    if item_damage_id <= get_repair_threshold():
        app_logger.info(f"check_item_damage_to_repair: True")
        return True
    else:
        app_logger.info(f"check_item_damage_to_repair: False")
        return False

def check_pickaxe_damage_to_repair(image_pickaxe: Optional[np.ndarray] = None) -> Optional[bool]:
    """
    Checks if the pickaxe needs repair based on its damage level.

    Args:
        image_pickaxe: An optional image of the pickaxe.

    Returns:
        True if the pickaxe needs repair, False otherwise, or None if an error occurs.
    """
    return check_item_damage_to_repair(image_pickaxe, get_pickaxe_image)

def check_axe_damage_to_repair(image_axe: Optional[np.ndarray] = None) -> Optional[bool]:
    """
    Checks if the axe needs repair based on its damage level.

    Args:
        image_axe: An optional image of the axe.

    Returns:
        True if the axe needs repair, False otherwise, or None if an error occurs.
    """
    return check_item_damage_to_repair(image_axe, get_axe_image)

def check_sword_damage_to_repair(image_sword: Optional[np.ndarray] = None) -> Optional[bool]:
    """
    Checks if the sword needs repair based on its damage level.

    Args:
        image_sword: An optional image of the sword.

    Returns:
        True if the sword needs repair, False otherwise, or None if an error occurs.
    """
    return check_item_damage_to_repair(image_sword, get_sword_image)

def find_item_pattern(image: np.ndarray, item_patterns: dict, threshold: float, item_name: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the best matching item pattern in a given image using template matching.

    Args:
        image (np.ndarray): The image to search for item patterns.
        item_patterns (dict): The dictionary of item patterns.
        threshold (float): The threshold value for template matching.
        item_name (str): The name of the item for logging purposes.

    Returns:
        Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: A tuple containing the top-left and bottom-right
        coordinates of the best matching item pattern, or None if no pattern exceeds the threshold.
    """
    app_logger.debug(f"find_{item_name}_pattern was used")
    app_logger.debug(f"used threshold: {threshold}")
    try:
        best_match = (None, 0, None)
        for key, pattern in item_patterns.items():
            if "mask" in key:
                continue
            result = cv2.matchTemplate(image, pattern, cv2.TM_CCORR_NORMED, mask=item_patterns["mask"])
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            app_logger.debug(f"{key} {item_name} max_val: {max_val} max_loc:{max_loc}")
            if max_val > best_match[1] and max_val > threshold:
                w, h = pattern.shape[1], pattern.shape[0]
                best_match = (max_loc, max_val, (w, h))
        if best_match[1] > threshold:
            top_left = best_match[0]
            w, h = best_match[2]
            bottom_right = (top_left[0] + w, top_left[1] + h)
            app_logger.debug(f'Best matching {item_name} found - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        app_logger.info(f'No {item_name} pattern exceeded the threshold.')
        return None
    except Exception as ex:
        app_logger.error(ex)

def find_pickaxe_pattern(image: np.ndarray, threshold: float = 0.92) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    return find_item_pattern(image, pickaxe_patterns, threshold, "pickaxe")

def find_axe_pattern(image: np.ndarray, threshold: float = 0.92) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    return find_item_pattern(image, axe_patterns, threshold, "axe")

def find_sword_pattern(image: np.ndarray, threshold: float = 0.92) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    return find_item_pattern(image, sword_patterns, threshold, "sword")

def find_obscure_matter_pattern(image: np.ndarray, threshold: float = 0.95) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    result = find_item_pattern(image, obscure_matter_patterns, threshold, "obscure-matter")
    if result is None:
        result = find_item_pattern(image, obscure_matters_patterns, threshold, "obscure-matters")
    return result
