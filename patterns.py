import array
from app_config import item_destruction_patterns_paths, slots_pattern_path, slots_pattern_mask_path, \
    pickaxe_patterns_paths, pickaxe_pattern_mask_path, eq_inventory_patterns_paths, chest_inventory_patterns_paths, \
    items_quantity_pattern, axe_patterns_paths, axe_pattern_mask_path, items_patterns_paths, sword_pattern_mask_path, \
    sword_patterns_paths, obscure_matter_patterns_paths, obscure_matter_pattern_mask_path, \
    obscure_matters_pattern_mask_path
from image_operations import convert_cv_image_to_gray, load_cv_image
from logger import app_logger
from typing import Dict, Any

item_destruction_patterns: Dict[str, Dict[str, Any]] = {}
slots_patterns: Dict[str, Any] = {}
pickaxe_patterns: Dict[str, Any] = {}
axe_patterns: Dict[str, Any] = {}
sword_patterns: Dict[str, Any] = {}
obscure_matter_patterns: Dict[str, Any] = {}
obscure_matters_patterns: Dict[str, Any] = {}
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

def load_item_patterns(patterns_dict: dict, patterns_paths: dict, mask_path: str, item_name: str) -> None:
    """
    Loads and stores item patterns and their masks for the application.

    Args:
        patterns_dict (dict): The global dictionary where patterns are to be stored.
        patterns_paths (dict): The dictionary of paths to the item patterns.
        mask_path (str): The path to the mask of the item patterns.
        item_name (str): The name of the item for logging purposes.

    This function handles the loading of item patterns and masks.
    """
    try:
        for key, path in patterns_paths.items():
            item_pattern = load_cv_image(path)
            patterns_dict[key] = item_pattern
            if item_pattern is None:
                app_logger.warning(f"Not loaded {item_name} pattern for key: {key}")
        # item_pattern_mask = convert_cv_image_to_gray(load_cv_image(mask_path))
        item_pattern_mask = load_cv_image(mask_path)
        patterns_dict["mask"] = item_pattern_mask
        if item_pattern_mask is None:
            app_logger.warning(f"Not loaded {item_name}_pattern_mask")
        app_logger.info(f"{item_name}_patterns was loaded")
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
    global pickaxe_patterns
    global axe_patterns
    global sword_patterns
    load_item_destruction_patterns()
    load_slots_patterns()
    load_item_patterns(pickaxe_patterns, pickaxe_patterns_paths, pickaxe_pattern_mask_path, "pickaxe")
    load_item_patterns(axe_patterns, axe_patterns_paths, axe_pattern_mask_path, "axe")
    load_item_patterns(sword_patterns, sword_patterns_paths, sword_pattern_mask_path, "sword")
    load_item_patterns(obscure_matter_patterns, obscure_matter_patterns_paths, obscure_matter_pattern_mask_path, "obscure-matter")
    load_item_patterns(obscure_matters_patterns, obscure_matter_patterns_paths, obscure_matters_pattern_mask_path, "obscure-matters")
    load_eq_inventory_patterns()
    load_chest_inventory_patterns()
    load_items_patterns()
