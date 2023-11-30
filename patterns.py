import array
from app_config import item_destruction_patterns_paths, slots_pattern_path, slots_pattern_mask_path, \
    pickaxe_pattern_path, pickaxe_pattern_mask_path, eq_inventory_patterns_paths, chest_inventory_patterns_paths, \
    items_quantity_pattern, axe_pattern_path, axe_pattern_mask_path
from image_operations import convert_cv_image_to_gray, load_cv_image
from logger import app_logger
from typing import Dict, Any

item_destruction_patterns: Dict[str, Dict[str, Any]] = {}
slots_patterns: Dict[str, Any] = {}
pickaxe_patterns: Dict[str, Any] = {}
axe_patterns: Dict[str, Any] = {}
eq_inventory_patterns: Dict[str, Any] = {}
chest_inventory_patterns: Dict[str, Any] = {}
items_patterns: Dict[str, Dict[str, Any]] = {}
items_quantity_mask: array.array = array.array

def load_slots_patterns() -> None:
    """
    Loads and stores slot patterns in grayscale for the application.

    This function converts and stores the main slot pattern and its mask from the predefined path.
    """
    global slots_patterns
    try:
        slots_patterns["slots_pattern"] = convert_cv_image_to_gray(load_cv_image(slots_pattern_path))
        slots_patterns["slots_pattern_mask"] = convert_cv_image_to_gray(load_cv_image(slots_pattern_mask_path))
        app_logger.info("slots_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_pickaxe_patterns() -> None:
    """
    Loads and stores pickaxe patterns and their masks for the application.

    Converts and stores the pickaxe pattern and its mask from the predefined path.
    """
    global pickaxe_patterns
    try:
        pickaxe_pattern = convert_cv_image_to_gray(load_cv_image(pickaxe_pattern_path))
        pickaxe_patterns["pickaxe_pattern"] = pickaxe_pattern
        if pickaxe_pattern is None:
            app_logger.warning("Not loaded pickaxe_pattern")
        pickaxe_pattern_mask = convert_cv_image_to_gray(load_cv_image(pickaxe_pattern_mask_path))
        pickaxe_patterns["pickaxe_pattern_mask"] = pickaxe_pattern_mask
        if pickaxe_pattern_mask is None:
            app_logger.warning("Not loaded pickaxe_pattern_mask")
        app_logger.info("pickaxe_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_axe_patterns() -> None:
    """
    Loads and stores axe patterns and their masks for the application.

    Similar to `load_pickaxe_patterns`, it handles the loading of axe patterns and masks.
    """
    global axe_patterns
    try:
        axe_pattern = convert_cv_image_to_gray(load_cv_image(axe_pattern_path))
        axe_patterns["axe_pattern"] = axe_pattern
        if axe_pattern is None:
            app_logger.warning("Not loaded axe_pattern")
        axe_pattern_mask = convert_cv_image_to_gray(load_cv_image(axe_pattern_mask_path))
        axe_patterns["axe_pattern_mask"] = axe_pattern_mask
        if axe_pattern_mask is None:
            app_logger.warning("Not loaded axe_pattern_mask")
        app_logger.info("axe_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_item_destruction_patterns() -> None:
    """
    Loads and stores item destruction bar patterns and their masks.

    Iterates over the predefined paths of item destruction patterns, loading each as grayscale images.
    """
    global item_destruction_patterns
    for pattern_key, pattern_value in item_destruction_patterns_paths.items():
        try:
            tmp_dict = {}
            # if pattern_value["pattern_path"]:
            #     pattern = convert_cv_image_to_gray(load_cv_image(pattern_value["pattern_path"]))
            #     tmp_dict["pattern"] = pattern
            # if pattern_value["pattern_mask_path"]:
            #     pattern_mask = convert_cv_image_to_gray(load_cv_image(pattern_value["pattern_mask_path"]))
            #     tmp_dict["pattern"] = pattern_mask
            if pattern_value["bar_path"]:
                bar = convert_cv_image_to_gray(load_cv_image(pattern_value["bar_path"])) #TODO: czy one powinny być wczytywane w skali szarości?
                tmp_dict["bar"] = bar
            if pattern_value["bar_mask_path"]:
                bar_mask = convert_cv_image_to_gray(load_cv_image(pattern_value["bar_mask_path"]))
                tmp_dict["bar_mask"] = bar_mask
            item_destruction_patterns[pattern_key] = tmp_dict
        except Exception as ex:
            app_logger.error(ex)
    app_logger.info("pickaxe_destruction_patterns was loaded")

def load_chest_inventory_patterns() -> None:
    """
    Loads and stores chest inventory patterns.

    This function loads each pattern defined in the `chest_inventory_patterns_paths` as grayscale images.
    """
    global chest_inventory_patterns
    try:
        for pattern_key, pattern_value in chest_inventory_patterns_paths.items():
                chest_inventory_patterns[pattern_key] = convert_cv_image_to_gray(load_cv_image(pattern_value))
        app_logger.info("eq_inventory_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_eq_inventory_patterns() -> None: #TODO: Wykestrachować wspólną część z funkcją load_chest_inventory_patterns() do osobnej funkcji
    """
    Loads and stores equipment inventory patterns.

    Functions similarly to `load_chest_inventory_patterns`.
    """
    global eq_inventory_patterns
    try:
        for pattern_key, pattern_value in eq_inventory_patterns_paths.items():
                eq_inventory_patterns[pattern_key] = convert_cv_image_to_gray(load_cv_image(pattern_value))
        app_logger.info("eq_inventory_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_items_patterns() -> None:
    """
    Loads and stores various item patterns along with their masks and colored versions.

    Processes the items' patterns, masks, and color versions for each item defined in `items_patterns_paths`, loads the quantity mask for items.
    """
    global items_patterns_paths
    global items_quantity_mask
    try:
        items_quantity_mask =convert_cv_image_to_gray(load_cv_image(items_quantity_pattern))
        for pattern_key, pattern_value in items_patterns_paths.items():
            items_patterns[pattern_key] = {}
            for key, path in pattern_value.items():
                image = load_cv_image(path)
                image_gray = convert_cv_image_to_gray(image)
                items_patterns[pattern_key][key] = image_gray
                if key == "pattern":
                    items_patterns[pattern_key][f"{key}_color"] = image
        app_logger.info("items_patterns was loaded")
    except Exception as ex:
        app_logger.error(ex)

def load_patterns_all() -> None:
    """
    Executes the loading of all patterns used in the application.

    Calls individual functions to load different sets of patterns like item destruction, slots, pickaxe, axe, equipment inventory, chest inventory, and item patterns.
    """
    load_item_destruction_patterns()
    load_slots_patterns()
    load_pickaxe_patterns()
    load_axe_patterns()
    load_eq_inventory_patterns()
    load_chest_inventory_patterns()
    load_items_patterns()
