import copy
import time
import cv2
import keyboard
import numpy as np
import pyautogui
from app_config import get_hotkey_inventory, get_eq_limit_to_stored
from image_operations import convert_cv_image_to_gray
from logger import app_logger
from patterns import eq_inventory_patterns
from screenshooter import get_last_screenshot

eq = {
    "width": None,
    "height": None,
}

bottom_frame = {
    "width": None,
    "height": None,
}

left_frame = {
    "width": None,
    "height": None,
}

horizontal_slot_frame = {
    "width": None,
    "height": None,
}

vertical_slot_frame = {
    "width": None,
    "height": None,
}

empty_item_slot = {
    "width": None,
    "height": None,
}

separation_frame = {
    "width": None,
    "height": None,
}

eq_slots_amount = 9
eq_inventory_amount = 27

def update_eq_patterns_sizes():
    """
    Updates the sizes of various equipment inventory patterns based on their image shapes.

    This function sets the global dictionaries for different components of the equipment inventory, such as the bottom frame, left frame, and slot frames, with their corresponding width and height obtained from the shapes of their respective images.
    """
    if eq_inventory_patterns["eq"] is not None:
        eq["width"], eq["height"] = eq_inventory_patterns["eq"].shape[1], eq_inventory_patterns["eq"].shape[0]
    if eq_inventory_patterns["bottom-frame"] is not None:
        bottom_frame["width"], bottom_frame["height"] = eq_inventory_patterns["bottom-frame"].shape[1], eq_inventory_patterns["bottom-frame"].shape[0]
    if eq_inventory_patterns["left-frame"] is not None:
        left_frame["width"], left_frame["height"] = eq_inventory_patterns["left-frame"].shape[1], eq_inventory_patterns["left-frame"].shape[0]
    if eq_inventory_patterns["horizontal-slot-frame"] is not None:
        horizontal_slot_frame["width"], horizontal_slot_frame["height"] = eq_inventory_patterns["horizontal-slot-frame"].shape[1], eq_inventory_patterns["horizontal-slot-frame"].shape[0]
    if eq_inventory_patterns["vertical-slot-frame"] is not None:
        vertical_slot_frame["width"], vertical_slot_frame["height"] = eq_inventory_patterns["vertical-slot-frame"].shape[1], eq_inventory_patterns["vertical-slot-frame"].shape[0]
    if eq_inventory_patterns["empty-item-slot"] is not None:
        empty_item_slot["width"], empty_item_slot["height"] = eq_inventory_patterns["empty-item-slot"].shape[1], eq_inventory_patterns["empty-item-slot"].shape[0]
    if eq_inventory_patterns["separation-frame"] is not None:
        separation_frame["width"], separation_frame["height"] = eq_inventory_patterns["separation-frame"].shape[1], eq_inventory_patterns["separation-frame"].shape[0]

def find_eq_inventory_pattern(image):
    """
    Finds the equipment inventory pattern in a given image.

    Args:
        image: The image in which the equipment inventory pattern is to be found.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found pattern, or None if not found.

    The function uses template matching to find the pattern and returns its coordinates if the match value is above a threshold.
    """
    global eq
    app_logger.debug("find_eq_inventory_pattern was used")
    threshold = 0.8
    try:
        image_gray = convert_cv_image_to_gray(copy.copy(image))
        result = cv2.matchTemplate(image_gray, eq_inventory_patterns["eq"], cv2.TM_CCOEFF_NORMED, mask=eq_inventory_patterns["eq_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f'eq_inventory - max_val: {max_val}')
        if max_val > threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + eq["width"], top_left[1] + eq["height"])
            app_logger.debug(f'eq_inventory was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('eq_inventory pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)

def get_inventory_image(image_screenshoot=None):
    """
    Retrieves the cropped inventory image from a given screenshot.

    Args:
        image_screenshoot: An optional screenshot image. If not provided, the function will take a new screenshot.

    Returns:
        A tuple containing the cropped inventory image, top-left, and bottom-right coordinates of the inventory, or None if not found.

    The function first finds the inventory pattern and then crops the image to return only the inventory portion.
    """
    app_logger.debug("get_inventory_image was used")
    if image_screenshoot is None:
        app_logger.debug("image_screenshoot is None - try get_last_screenshot()")
        image = copy.copy(get_last_screenshot())
    else:
        image = copy.copy(image_screenshoot)
    try:
        eq_inventory_pattern = find_eq_inventory_pattern(image)
        if eq_inventory_pattern:
            inventory_top_left, inventory_bottom_right = eq_inventory_pattern
            inventory_x1, inventory_y1 = inventory_top_left
            inventory_x2, inventory_y2 = inventory_bottom_right
            cropped_inventory_image = image[inventory_y1:inventory_y2, inventory_x1:inventory_x2]
            app_logger.debug(f"inventory_top_left: {inventory_top_left} inventory_bottom_right: {inventory_bottom_right}")
            return cropped_inventory_image, inventory_top_left, inventory_bottom_right
        else:
            app_logger.debug(f"eq_inventory_pattern is {eq_inventory_pattern}")
        return None
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_inventory_slots_images(inventory_image=None, slots_coordinates=None):
    """
    Obtains images of individual inventory slots.

    Args:
        inventory_image: An optional pre-captured inventory image.
        slots_coordinates: Optional pre-calculated coordinates of the inventory slots.

    Returns:
        A list of images, each representing an individual inventory slot, or None if an error occurs.

    The function can calculate slots coordinates if not provided and then crops the inventory image to get each slot's image.
    """
    app_logger.debug("get_inventory_slots_images was used")
    try:
        if inventory_image is None:
            app_logger.debug("inventory_image is None - try get_inventory_image()")
            inventory_image, inventory_top_left, inventory_bottom_right = get_inventory_image()
        else:
            inventory_image = copy.copy(inventory_image)
        if slots_coordinates is None:
            app_logger.debug("slots_coordinates is None - try get_slots_inventory_coordinates(inventory_image)")
            slots_coordinates = get_slots_inventory_coordinates(inventory_image)
        slots_images = []
        for slot in slots_coordinates:
            slot_top_left, slot_bottom_right = slot
            slot_x1, slot_y1 = slot_top_left
            slot_x2, slot_y2 = slot_bottom_right
            cropped_slot_image = inventory_image[slot_y1:slot_y2, slot_x1:slot_x2]
            slots_images.append(cropped_slot_image)
        app_logger.debug(f"slots_images have {len(slots_images)} elements")
        return slots_images
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_slots_inventory_coordinates(inventory_image=None):
    """
    Calculates the coordinates of all inventory slots in the equipment inventory image.

    Args:
        inventory_image: An optional pre-captured inventory image.

    Returns:
        A list of tuples, each containing the top-left and bottom-right coordinates of an inventory slot, or None if an error occurs.

    The function calculates the coordinates based on the known sizes and arrangements of the slots in the inventory.
    """
    app_logger.debug("get_slots_inventory_coordinates was used")
    try:
        if inventory_image is None:
            app_logger.debug("inventory_image is None - try get_inventory_image()")
            inventory_image, inventory_top_left, inventory_bottom_right = get_inventory_image()
        else:
            inventory_image = copy.copy(inventory_image)
        inventory_width, inventory_height = inventory_image.shape[1], inventory_image.shape[0]
        app_logger.debug(f"inventory_width: {inventory_width} inventory_height: {inventory_height}")
        slots_coordinates = []
        start_slot_x1 = left_frame["width"]
        start_slot_y2 = inventory_height - bottom_frame["height"]
        start_slot_y1 = start_slot_y2-empty_item_slot["height"]
        start_slot_x2 = start_slot_x1+empty_item_slot["width"]
        tmp_width_value = empty_item_slot["width"]+vertical_slot_frame["width"]
        for x in range(9):
            slots_coordinates.append(
                (
                    (start_slot_x1 + tmp_width_value * x, start_slot_y1),
                    (start_slot_x2 + tmp_width_value * x, start_slot_y2)
                )
            )
        start_slot_y1 = start_slot_y1 - separation_frame["height"] - empty_item_slot["height"]
        start_slot_y2 = start_slot_y2 - separation_frame["height"] - empty_item_slot["height"]
        tmp_height_value = empty_item_slot["height"] + horizontal_slot_frame["height"]
        for y in range(3):
            for x in range(9):
                slots_coordinates.append(
                    (
                        (start_slot_x1 + tmp_width_value * x, start_slot_y1 - tmp_height_value * y),
                        (start_slot_x2 + tmp_width_value * x, start_slot_y2 - tmp_height_value * y)
                    )
                )
        app_logger.debug(f"slots_coordinates: {slots_coordinates}")
        return slots_coordinates
    except Exception as ex:
        app_logger.error(ex)
        return None

def check_slot_free(slot_image):
    """
    Checks if a given slot image represents an empty slot.

    Args:
        slot_image: The image of the slot to be checked.

    Returns:
        True if the slot is free, False if it is occupied, or None if an error occurs.

    The function compares the slot image with a pattern of an empty slot to determine if it is free.
    """
    app_logger.debug("check_slot_free was used")
    try:
        slot_image_gray = convert_cv_image_to_gray(slot_image)
        abs_diff = cv2.absdiff(slot_image_gray, eq_inventory_patterns["empty-item-slot"])
        mean_diff = np.mean(abs_diff)
        app_logger.debug(f"mean_diff: {mean_diff}")
        threshold = 5
        is_free = mean_diff < threshold
        app_logger.debug(f"is_free is {is_free}")
        return is_free
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_inventory_occupancy_value(slots_images_list):
    """
    Calculates the number of occupied slots in the inventory.

    Args:
        slots_images_list: A list of images, each representing an individual inventory slot.

    Returns:
        The number of slots that are occupied, or None if an error occurs.

    The function iterates over the slot images and checks each one to determine if it is occupied.
    """
    app_logger.debug("get_inventory_occupancy_value was used")
    try:
        slots_fully = 0
        for slot_image in slots_images_list:
            if not check_slot_free(slot_image):
                slots_fully = slots_fully + 1
        app_logger.debug(f"slots_fully: {slots_fully}")
        return slots_fully
    except Exception as ex:
        app_logger.error(ex)

def get_inventory_occupancy_list(slots_images_list):
    """
    Creates a list indicating the occupancy status of each slot in the inventory.

    Args:
        slots_images_list: A list of images, each representing an individual inventory slot.

    Returns:
        A list of boolean values indicating the occupancy status (True for free, False for occupied) of each slot, or None if an error occurs.
    """
    app_logger.debug("get_inventory_occupancy_list was used")
    try:
        slots_occupancy = []
        for slot_image in slots_images_list:
            slots_occupancy.append(check_slot_free(slot_image))
        app_logger.debug(f"slots_occupancy: {slots_occupancy}")
        return slots_occupancy
    except Exception as ex:
        app_logger.error(ex)

def check_inventory_full():
    """
    Checks if the inventory is full based on a set limit.

    Returns:
        True if the inventory is full, False if not, or None if the inventory pattern was not found or an error occurs.

    The function calculates the number of occupied slots and compares it with a predefined limit to determine if the inventory is full.
    """
    app_logger.debug("check_inventory_full was used")
    try:
        keyboard.press_and_release(get_hotkey_inventory())
        time.sleep(0.5)
        x = -(eq["width"]/2)
        y = -(eq["height"]/2)
        pyautogui.move(x, y)
        time.sleep(1)
        inventory_image_result = get_inventory_image()
        time.sleep(0.5)
        keyboard.press_and_release(get_hotkey_inventory())
        if inventory_image_result is not None:
            cropped_inventory_image, inventory_top_left, inventory_bottom_right = inventory_image_result
            slots_coordinates = get_slots_inventory_coordinates(cropped_inventory_image)
            app_logger.debug(f"slots_coordinates: {slots_coordinates}")
            slots_images = get_inventory_slots_images(cropped_inventory_image, slots_coordinates)
            app_logger.debug(f"slots_images have {len(slots_images)} elements")
            slots_full_value = get_inventory_occupancy_value(slots_images)
            app_logger.info(f"slots_full_value: {slots_full_value}")
            if slots_full_value >= get_eq_limit_to_stored():
                app_logger.debug(f"slots_full_value: {slots_full_value} is greater than or equal to eq_limit_to_stored: {get_eq_limit_to_stored()} - return True")
                return True
            else:
                app_logger.debug(
                    f"slots_full_value: {slots_full_value} is less than eq_limit_to_stored: {get_eq_limit_to_stored()} - return False")
                return False
        else:
            app_logger.warning("check_inventory_full - Inventory pattern was not found.")
            return None
    except Exception as ex:
        app_logger.error(ex)
        return None
