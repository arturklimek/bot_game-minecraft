import cv2
import numpy as np
from image_operations import convert_cv_image_to_gray
from logger import app_logger
from patterns import item_destruction_patterns


def analyze_damage_level(item_image: np.ndarray) -> int:
    """
    Analyzes the damage level of a tool or item based on its image.

    Args:
        item_image (numpy.ndarray): An image of the item or tool whose damage level is to be analyzed.

    This function processes the provided image to determine the damage level of the item. It uses template matching to compare the item's image against a set of predefined patterns that represent different levels of item damage. Each pattern corresponds to a specific damage level.

    Returns:
        int: An index representing the best match among the damage level patterns. This index corresponds
        to the estimated damage level of the item.

    Note:
        The function relies on a set of predefined patterns (item_destruction_patterns) that should
        cover all possible damage states of the item.
    """
    gray_image = convert_cv_image_to_gray(item_image)
    scores = []
    for pattern_key, pattern_value in item_destruction_patterns.items():
        if "bar" in pattern_value and "bar_mask" in pattern_value:
            bar = pattern_value["bar"]
            bar_mask = pattern_value["bar_mask"]
            result = cv2.matchTemplate(gray_image, bar, cv2.TM_CCORR_NORMED, mask=bar_mask)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            scores.append(max_val)
    best_match_index = np.argmax(scores)
    best_match_score = scores[best_match_index]
    app_logger.debug(f"best_match_index: {best_match_index} best_match_score: {best_match_score}")
    return best_match_index

