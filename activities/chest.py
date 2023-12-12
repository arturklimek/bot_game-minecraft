import copy
import time
from datetime import datetime
from typing import Optional, Tuple, List

import cv2
import numpy as np
import pyautogui
import pygetwindow
from app_config import get_game_window_name, get_save_images_flags
from image_operations import convert_cv_image_to_gray, save_cv_image, save_image_for_function
from logger import app_logger
from patterns import chest_inventory_patterns, items_patterns
from screenshooter import get_last_screenshot

chest_inventory_elements = {
    "chest-small": {},
    "chest-big": {},
    "bottom-frame": {},
    "left-frame": {},
    "horizontal-slot-frame": {},
    "vertical-slot-frame": {},
    "empty-item-slot": {},
    "separation-frame_1": {},
    "separation-frame_2": {},
}

eq_slots_amount = 9
eq_inventory_amount = 27
chest_big_inventory_amount = 54
chest_small_inventory_amount = 27

def set_dimensions(element: dict, pattern: np.ndarray) -> None:
    """
    Sets the dimensions (width and height) of an element based on the given pattern.

    Args:
        element: The dictionary element to set dimensions for.
        pattern: The pattern image used to determine dimensions.
    """
    if pattern is not None:
        element["width"], element["height"] = pattern.shape[1], pattern.shape[0]

def update_chest_patterns_sizes() -> None:
    """
    Updates the sizes of chest inventory elements based on the defined chest inventory patterns.
    """
    for element_key in chest_inventory_elements.keys():
        if element_key in chest_inventory_patterns:
            set_dimensions(chest_inventory_elements[element_key], chest_inventory_patterns[element_key])

def find_chest_big_pattern(image: np.ndarray, threshold: float = 0.75) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Finds the 'big chest' pattern in a given image using template matching.

    Args:
        image: The image to search for the 'big chest' pattern.
        threshold: The threshold value for template matching, default is 0.75.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found 'big chest' pattern, or None if not found.
    """
    global chest_inventory_elements
    app_logger.debug("find_chest_big_pattern was used")
    app_logger.debug(f"threshold: {threshold}")
    try:
        save_image_for_function("find_chest_big_pattern", "image", image)
        image_gray = convert_cv_image_to_gray(copy.copy(image))
        result = cv2.matchTemplate(image_gray, chest_inventory_patterns["chest-big"], cv2.TM_CCOEFF_NORMED, mask=chest_inventory_patterns["chest-big_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f'chest_big - max_val: {max_val} max_loc: {max_loc}')
        if max_val > threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + chest_inventory_elements["chest-big"]["width"], top_left[1] + chest_inventory_elements["chest-big"]["height"])
            app_logger.debug(f'chest_big was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('chest_big pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)

def get_chest_big_image(image_screenshoot: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    """
    Retrieves the image of a 'big chest' from a screenshot or a given image.

    Args:
        image_screenshoot: An optional screenshot image. If not provided, the function will take a new screenshot.

    Returns:
        A tuple containing the cropped chest image, top-left, and bottom-right coordinates of the chest, or None if not found.
    """
    app_logger.debug("get_chest_big_image was used")
    if image_screenshoot is None:
        app_logger.debug("image_screenshoot is None - try get_last_screenshot()")
        image = copy.copy(get_last_screenshot())
    else:
        image = copy.copy(image_screenshoot)
    try:
        save_image_for_function("get_chest_big_image", "image_screenshoot", image_screenshoot)
        chest_pattern = find_chest_big_pattern(image)
        if chest_pattern:
            chest_top_left, chest_bottom_right = chest_pattern
            chest_x1, chest_y1 = chest_top_left
            chest_x2, chest_y2 = chest_bottom_right
            cropped_chest_image = image[chest_y1:chest_y2, chest_x1:chest_x2]
            save_image_for_function("get_chest_big_image", "cropped_chest_image", cropped_chest_image)
            app_logger.debug(f"chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right}")
            return cropped_chest_image, chest_top_left, chest_bottom_right
        else:
            app_logger.debug("chest_pattern is None")
        return None
    except Exception as ex:
        app_logger.error(ex)
        return None

def find_chest_small_pattern(image: np.ndarray, threshold: float = 0.75) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: #TODO: zrefactorować tak aby nie powielać kodu między funkcjami
    """
    Finds the 'small chest' pattern in a given image using template matching.

    Args:
        image: The image to search for the 'small chest' pattern.
        threshold: The threshold value for template matching, default is 0.75.

    Returns:
        A tuple containing the top-left and bottom-right coordinates of the found 'small chest' pattern, or None if not found.
    """
    global chest_inventory_elements
    app_logger.debug("find_chest_small_pattern was used")
    app_logger.debug(f"threshold: {threshold}")
    try:
        save_image_for_function("find_chest_small_pattern", "image", image)
        image_gray = convert_cv_image_to_gray(copy.copy(image))
        result = cv2.matchTemplate(image_gray, chest_inventory_patterns["chest-small"], cv2.TM_CCOEFF_NORMED, mask=chest_inventory_patterns["chest-small_mask"])
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        app_logger.debug(f'chest_small - max_val: {max_val} max_loc: {max_loc}')
        if max_val > threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + chest_inventory_elements["chest-small"]["width"], top_left[1] + chest_inventory_elements["chest-small"]["height"])
            app_logger.debug(f'chest_small was found in - top_left: {top_left} bottom_right: {bottom_right}')
            return top_left, bottom_right
        else:
            app_logger.info('chest_small pattern was not found.')
            return None
    except Exception as ex:
        app_logger.error(ex)

def get_chest_small_image(image_screenshoot: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]]:
    """
    Retrieves the image of a 'small chest' from a screenshot or a given image.

    Args:
        image_screenshoot: An optional screenshot image. If not provided, the function will take a new screenshot.

    Returns:
        A tuple containing the cropped chest image, top-left, and bottom-right coordinates of the chest, or None if not found.
    """
    app_logger.debug("get_chest_small_image was used")
    if image_screenshoot is None:
        app_logger.debug("image_screenshoot is None - try get_last_screenshot()")
        image = copy.copy(get_last_screenshot())
    else:
        image = copy.copy(image_screenshoot)
    try:
        save_image_for_function("get_chest_small_image", "image_screenshoot", image_screenshoot)
        chest_pattern = find_chest_small_pattern(image)
        if chest_pattern:
            chest_top_left, chest_bottom_right = chest_pattern
            chest_x1, chest_y1 = chest_top_left
            chest_x2, chest_y2 = chest_bottom_right
            cropped_chest_image = image[chest_y1:chest_y2, chest_x1:chest_x2]
            app_logger.debug(f"chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right}")
            return cropped_chest_image, chest_top_left, chest_bottom_right
        else:
            app_logger.debug("chest_pattern is None")
        return None
    except Exception as ex:
        app_logger.error(ex)
        return None

def check_and_get_chest_image(image_screenshoot: Optional[np.ndarray] = None) -> Optional[Tuple[np.ndarray, Tuple[int, int], Tuple[int, int], int]]:
    """
    Checks for and retrieves the image of either a 'big chest' or 'small chest' from a screenshot or a given image.

    Args:
        image_screenshoot: An optional screenshot image. If not provided, the function will take a new screenshot.

    Returns:
        A tuple containing the cropped chest image, top-left, bottom-right coordinates, and chest size, or None if not found.
    """
    app_logger.debug("check_and_get_chest_image was used")
    if image_screenshoot is None:
        app_logger.debug("image_screenshoot is None - try get_last_screenshot()")
        image = copy.copy(get_last_screenshot())
    else:
        image = copy.copy(image_screenshoot)
    try:
        save_image_for_function("check_and_get_chest_image", "image", image)
        chest_pattern = find_chest_big_pattern(image)
        chest_size = chest_big_inventory_amount
        if not chest_pattern:
            chest_pattern = find_chest_small_pattern(image)
            chest_size = chest_small_inventory_amount
        if chest_pattern:
            chest_top_left, chest_bottom_right = chest_pattern
            chest_x1, chest_y1 = chest_top_left
            chest_x2, chest_y2 = chest_bottom_right
            cropped_chest_image = image[chest_y1:chest_y2, chest_x1:chest_x2]
            save_image_for_function("check_and_get_chest_image", "cropped_chest_image", cropped_chest_image)
            app_logger.debug(f"chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right} chest_size: {chest_size}")
            return cropped_chest_image, chest_top_left, chest_bottom_right, chest_size
        app_logger.debug("chest_pattern is None")
        return None
    except Exception as ex:
        app_logger.error(ex)
        return None

def get_slots_chest_coordinates(chest_image: Optional[np.ndarray] = None, chest_size: int = chest_big_inventory_amount) -> Optional[List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    """
    Calculates the coordinates of each slot in a chest inventory image.

    Args:
        chest_image: An optional image of a chest inventory. If not provided, the function will attempt to capture a new image.
        chest_size: The total number of slots in the chest, default is the size of a big chest.

    Returns:
        A list of tuples containing the top-left and bottom-right coordinates of each slot in the chest inventory.
    """
    app_logger.debug("get_slots_chest_coordinates was used")
    try:
        if chest_image is None:
            app_logger.debug("chest_image is None - try check_and_get_chest_image()")
            chest_image, chest_top_left, chest_bottom_right, chest_size = check_and_get_chest_image()
        else:
            chest_image = copy.copy(chest_image)
        save_image_for_function("get_slots_chest_coordinates", "chest_image", chest_image)
        chest_width, chest_height = chest_image.shape[1], chest_image.shape[0]
        slots_coordinates = []
        start_slot_x1 = chest_inventory_elements["left-frame"]["width"]
        start_slot_y2 = chest_height - chest_inventory_elements["bottom-frame"]["height"]
        start_slot_y1 = start_slot_y2-chest_inventory_elements["empty-item-slot"]["height"]
        start_slot_x2 = start_slot_x1+chest_inventory_elements["empty-item-slot"]["width"]
        tmp_width_value = chest_inventory_elements["empty-item-slot"]["width"]+chest_inventory_elements["vertical-slot-frame"]["width"]
        for x in range(9):
            slots_coordinates.append(
                (
                    (start_slot_x1 + tmp_width_value * x, start_slot_y1),
                    (start_slot_x2 + tmp_width_value * x, start_slot_y2)
                )
            )
        start_slot_y1 = start_slot_y1 - chest_inventory_elements["separation-frame_1"]["height"] - chest_inventory_elements["empty-item-slot"]["height"]
        start_slot_y2 = start_slot_y2 - chest_inventory_elements["separation-frame_1"]["height"] - chest_inventory_elements["empty-item-slot"]["height"]
        tmp_height_value = chest_inventory_elements["empty-item-slot"]["height"] + chest_inventory_elements["horizontal-slot-frame"]["height"]
        for y in range(3):
            for x in range(9):
                slots_coordinates.append(
                    (
                        (start_slot_x1 + tmp_width_value * x, start_slot_y1 - tmp_height_value * y),
                        (start_slot_x2 + tmp_width_value * x, start_slot_y2 - tmp_height_value * y)
                    )
                )
        start_slot_y1 = start_slot_y1 - chest_inventory_elements["separation-frame_2"]["height"] - (chest_inventory_elements["empty-item-slot"]["height"]*3+chest_inventory_elements["horizontal-slot-frame"]["height"]*2)
        start_slot_y2 = start_slot_y2 - chest_inventory_elements["separation-frame_2"]["height"] - (chest_inventory_elements["empty-item-slot"]["height"]*3+chest_inventory_elements["horizontal-slot-frame"]["height"]*2)
        for y in range(int(chest_size/9)):
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

def get_chest_slots_images(chest_image: Optional[np.ndarray] = None, slots_coordinates: Optional[List[Tuple[Tuple[int, int], Tuple[int, int]]]] = None) -> Optional[List[np.ndarray]]:
    """
    Retrieves images of individual slots in a chest inventory based on their coordinates.

    Args:
        chest_image: An optional image of a chest inventory. If not provided, the function will attempt to capture a new image.
        slots_coordinates: Optional pre-calculated slots coordinates. If not provided, coordinates are calculated.

    Returns:
        A list of images representing individual slots in the chest inventory.
    """
    app_logger.debug("get_chest_slots_images was used")
    try:
        if chest_image is None:
            app_logger.debug("chest_image is None - try check_and_get_chest_image()")
            chest_image, chest_top_left, chest_bottom_right, chest_size = check_and_get_chest_image()
        else:
            chest_image = copy.copy(chest_image)
        save_image_for_function("get_chest_slots_images", "chest_image", chest_image)
        if slots_coordinates is None:
            app_logger.debug("slots_coordinates is None")
            chest_width, chest_height = chest_image.shape[1], chest_image.shape[0]
            if chest_height == chest_inventory_elements["chest-small"]["height"]:
                chest_size = chest_small_inventory_amount
            else:
                chest_size = chest_big_inventory_amount
            slots_coordinates = get_slots_chest_coordinates(chest_image, chest_size)
        slots_images = []
        for slot in slots_coordinates:
            slot_top_left, slot_bottom_right = slot
            slot_x1, slot_y1 = slot_top_left
            slot_x2, slot_y2 = slot_bottom_right
            cropped_slot_image = chest_image[slot_y1:slot_y2, slot_x1:slot_x2]
            slots_images.append(cropped_slot_image)
        app_logger.debug(f"slots_images have {len(slots_images)} elements")
        return slots_images
    except Exception as ex:
        app_logger.error(ex)
        return None

def find_item_pattern_in_item_image(item_image: np.ndarray, items_quantity_mask: np.ndarray, patterns: dict = items_patterns, threshold_pixels: float = 0.95, threshold_pattern: float = 0.23) -> Optional[str]:
    """
    Identifies an item pattern within an item image.

    Args:
        item_image: The image of the item slot.
        items_quantity_mask: The mask used to ignore quantity indicators in the slot.
        patterns: A dictionary of item patterns to match against, default is 'items_patterns'.
        threshold_pixels: The pixel match threshold, default is 0.95.
        threshold_pattern: The overall pattern match threshold, default is 0.26.

    Returns:
        The key of the identified item pattern if a match is found, None otherwise.
    """
    try:
        app_logger.debug("find_item_pattern_in_item_image was used")
        app_logger.debug(f"threshold_pixels: {threshold_pixels}")
        app_logger.debug(f"threshold_pattern: {threshold_pattern}")
        save_image_for_function("find_item_pattern_in_item_image", "item_image", item_image)
        quantity_mask_inverted = cv2.bitwise_not(items_quantity_mask)
        best_match = (None, 0)
        for key, pattern_info in patterns.items():
            pattern_color = pattern_info['pattern_color']
            mask = pattern_info['mask']
            if pattern_color.shape[:2] != (48, 48) or mask.shape[:2] != (48, 48):
                continue
            combined_mask = cv2.bitwise_and(mask, quantity_mask_inverted)
            num_pixels_to_check = np.sum(combined_mask > 0)
            pattern_masked = cv2.bitwise_and(pattern_color, pattern_color, mask=combined_mask)
            item_image_masked = cv2.bitwise_and(item_image, item_image, mask=combined_mask)
            num_compatible_pixels = 0
            for i in range(48):
                for j in range(48):
                    if combined_mask[i, j] > 0:
                        pixel_diff = np.abs(item_image_masked[i, j] - pattern_masked[i, j])
                        if np.all(pixel_diff < (255 * (1 - threshold_pixels))):
                            num_compatible_pixels += 1
            match_ratio = num_compatible_pixels / num_pixels_to_check
            app_logger.debug(f"key: {key} match_ratio: {match_ratio}")
            if match_ratio > threshold_pattern and match_ratio > best_match[1]:
                best_match = (key, match_ratio)
        app_logger.debug(f"{best_match[0]} - best_match ratio: {best_match[1]}")
        return best_match[0] if best_match[1] > threshold_pattern else None
    except Exception as ex:
        app_logger.error(ex)

def get_game_window_coordinates(window_title: str) -> Optional[Tuple[int, int]]:
    """
    Retrieves the screen coordinates (top left corner) of a game window based on its title.

    Args:
        window_title: The title of the game window.

    Returns:
        A tuple containing the x and y coordinates of the game window, or None if the window is not found.
    """
    app_logger.debug("get_game_window_coordinates was used")
    try:
        game_window = pygetwindow.getWindowsWithTitle(window_title)[0]
        return game_window.left, game_window.top
    except IndexError as ie:
        app_logger.error(ie)
        app_logger.debug(f"The window '{window_title}' was not found.")
        return None

def shift_click_at_coordinates_in_game_window(slots_coordinates: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
    """
    Performs a shift-click action at specified coordinates within a game window.

    Args:
        slots_coordinates: A tuple containing the top-left and bottom-right coordinates of the slot to be clicked.

    This function calculates the actual screen coordinates based on the game window's position and performs a shift-click action.
    """
    app_logger.debug("shift_click_at_coordinates_in_game_window was used")
    app_logger.debug(f"Taked slots_coordinates: {slots_coordinates}")
    window_coordinates = get_game_window_coordinates(get_game_window_name())
    if window_coordinates is None:
        app_logger.debug(f"window_coordinates is: {window_coordinates}")
        return
    window_x, window_y = window_coordinates
    slot_top_left, slot_bottom_right = slots_coordinates
    slot_x1, slot_y1 = slot_top_left
    slot_x2, slot_y2 = slot_bottom_right
    click_x = (slot_x1 + slot_x2) // 2 + window_x
    click_y = (slot_y1 + slot_y2) // 2 + window_y
    app_logger.debug(f"click_x: {click_x} click_y: {click_y}")
    shift_click_at_coordinates(click_x, click_y)

def shift_click_at_coordinates(click_x: int, click_y: int) -> None:
    """
    Performs a shift-click action at specified screen coordinates.

    Args:
        click_x: The x coordinate on the screen where the click should be performed.
        click_y: The y coordinate on the screen where the click should be performed.

    This function moves the mouse to the specified coordinates, holds down the shift key, performs a click, and then releases the shift key.
    """
    app_logger.debug("shift_click_at_coordinates was used")
    time.sleep(0.1)
    pyautogui.moveTo(click_x, click_y)
    app_logger.debug(f"click_x: {click_x} click_y: {click_y}")
    time.sleep(0.1)
    pyautogui.keyDown('shift')
    app_logger.debug(f"Press 'shift'")
    time.sleep(0.1)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.keyUp('shift')
    app_logger.debug(f"Release 'shift'")

def calc_and_get_screenshoot_sloot_coordinates(slot_coordinates: Tuple[Tuple[int, int], Tuple[int, int]], chest_top_left: Tuple[int, int], chest_bottom_right: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Calculates the absolute screen coordinates for a slot based on its position within a chest inventory.

    Args:
        slot_coordinates: A tuple containing the top-left and bottom-right coordinates of the slot within the chest image.
        chest_top_left: The top-left coordinates of the chest inventory on the screen.
        chest_bottom_right: The bottom-right coordinates of the chest inventory on the screen.

    Returns:
        A tuple containing the updated top-left and bottom-right coordinates of the slot in screen coordinates.
    """
    app_logger.debug(f"calc_and_get_screenshoot_sloot_coordinates was used - slot_coordinates: {slot_coordinates} chest_top_left: {chest_top_left} chest_bottom_right: {chest_bottom_right}")
    slot_top_left, slot_bottom_right = slot_coordinates
    slot_x1, slot_y1 = slot_top_left
    slot_x2, slot_y2 = slot_bottom_right
    chest_x1, chest_y1 = chest_top_left
    chest_x2, chest_y2 = chest_bottom_right
    slot_x1 = slot_x1 + chest_x1
    slot_x2 = slot_x2 + chest_x1
    slot_y1 = slot_y1 + chest_y1
    slot_y2 = slot_y2 + chest_y1
    new_slot_coordinates = (
            (slot_x1, slot_y1),
            (slot_x2, slot_y2)
        )
    app_logger.debug(f"new_slot_coordinates: {new_slot_coordinates}")
    return new_slot_coordinates
