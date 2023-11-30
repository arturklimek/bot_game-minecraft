import os
from typing import Dict, Set, List

import yaml
import urllib.parse
from logger import app_logger

APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR_PATH = os.path.join(APP_PATH, 'outputs')
PATTERNS_DIR_PATH = os.path.join(APP_PATH, 'patterns')

game_window_name = 'Minecraft'

def get_game_window_name() -> str:
    return game_window_name

config_file_path = os.path.join(APP_PATH, 'config.yaml')

def get_config_file_path() -> str:
    return config_file_path

command_spawn = '/spawn'
command_home_repair = '/home repair'
command_home_mining = '/home mine'
command_home_chest = '/home chest'
command_home_farm = '/home farm'
command_home_tmp = '/home tmp'
command_sell_inventory = '/sellall inventory'

command_sethome = "/sethome"

def get_command_spawn() -> str:
    return command_spawn

def get_command_home_repair() -> str:
    return command_home_repair

def get_command_home_mining() -> str:
    return command_home_mining

def get_command_home_chest() -> str:
    return command_home_chest

def get_command_home_farm() -> str:
    return command_home_farm

def get_command_home_tmp() -> str:
    return command_home_tmp

def get_command_sell_inventory() -> str:
    return command_sell_inventory

def get_command_sethome() -> str:
    return command_sethome

autoclicker_delay_ms = 10

def get_autoclicker_delay_ms() -> int:
    return autoclicker_delay_ms

afk_breaks_flag = False

def get_afk_breaks_flag() -> bool:
    return afk_breaks_flag

pattern_settings = {
    'width': 1920,
    'height': 1080,
    'texture_pack': 'Faithful64x', #Recommended Faithful64x - tested at 1920x1080
    'eq_size': 3
}

def get_pattern_settings() -> Dict[str, any]:
    return pattern_settings

slots_pattern_path = os.path.join(PATTERNS_DIR_PATH, f'eq-slots_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png')
slots_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'eq-slots_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')

pickaxe_pattern_path = os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full.png')
pickaxe_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_mask.png')

axe_pattern_path = os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full.png')
axe_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_mask.png')

repair_threshold = 2
repair_mining_pickaxe_frequency = 15

def get_repair_threshold() -> int:
    return repair_threshold

def get_repair_mining_pickaxe_frequency() -> int:
    return repair_mining_pickaxe_frequency

# farm_toggle = False
# farm_frequency = 25
farm_number = 2
farm_floors_number = 15
farm_floor_time_moving = 34

tmp_home_flag = True

def get_farm_number() -> int:
    return farm_number

def get_farm_floors_number() -> int:
    return farm_floors_number

def get_farm_floor_time_moving() -> int:
    return farm_floor_time_moving

def get_tmp_home_flag() -> bool:
    return tmp_home_flag

screenshots_frequency = 0.5

def get_screenshots_frequency() -> float:
    return screenshots_frequency

hotkey_esc = 1
hotkey_enter = 28
hotkey_chat = 20
hotkey_inventory = 18
hotkey_moving_up = 17
hotkey_moving_down = 31
hotkey_moving_left = 30
hotkey_moving_right = 32
hotkeys_slots = {
    1: 2,
    2: 3,
    3: 4,
    4: 5,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10
}

def get_hotkey_esc() -> int:
    return hotkey_esc

def get_hotkey_enter() -> int:
    return hotkey_enter

def get_hotkey_chat() -> int:
    return hotkey_chat

def get_hotkey_inventory() -> int:
    return hotkey_inventory

def get_hotkey_moving_up() -> int:
    return hotkey_moving_up

def get_hotkey_moving_down() -> int:
    return hotkey_moving_down

def get_hotkey_moving_left() -> int:
    return hotkey_moving_left

def get_hotkey_moving_right() -> int:
    return hotkey_moving_right

def get_hotkeys_slots() -> Dict[int, int]:
    return hotkeys_slots

button_autoclicker_lpm = 79
button_autoclicker_ppm = 80
button_mine_procedure = 78
button_farm_procedure = 69

def get_button_autoclicker_lpm() -> int:
    return button_autoclicker_lpm

def get_button_autoclicker_ppm() -> int:
    return button_autoclicker_ppm

def get_button_mine_procedure() -> int:
    return button_mine_procedure

def get_button_farm_procedure() -> int:
    return button_farm_procedure

protected_slots = set([7,8,9])

def get_protected_slots():
    return protected_slots

def set_protected_slots(new_protected_slots: Set[int]) -> None:
    global protected_slots
    protected_slots = new_protected_slots

moving_time = 10
moving_hold_shift = False

def get_moving_time() -> int:
    return moving_time

def get_moving_hold_shift() -> bool:
    return moving_hold_shift

eq_limit_to_stored = 33

def get_eq_limit_to_stored() -> int:
    return eq_limit_to_stored

items_stored_list = ["diamond", "emerald", "gold-ore", "iron-ingot", "iron-ore"]

def get_items_stored_list():
    return items_stored_list

def set_items_stored_list(new_items_stored_list: List[str]) -> None:
    global items_stored_list
    items_stored_list = new_items_stored_list

chat_messages_flag = False
chat_messages = ['&6&lUWAGA! &f&lKupię &9&lMroczna Materia &7- &e&l2000&6&l$ &f&lza sztukę! &7- &b&l/msg MineArturVIP &7- &f&lNie ma mnie? Nie odpisuję? Napisz na DSC: &b&lMineArturVIP#6699 &f&llub do innego członka &7[&b&lS&f&lB&7&l-&f&lM&b&laf&9&lia&7]']
chat_messages_frequency_min = 15

def get_chat_messages_flag() -> bool:
    return chat_messages_flag

def get_chat_messages() -> List[str]:
    return chat_messages

def get_chat_messages_frequency_min() -> int:
    return chat_messages_frequency_min

eq_inventory_patterns_paths = {
    "eq": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
    "eq_mask": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png'),
    "bottom-frame": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bottom-frame.png'),
    "left-frame": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_left-frame.png'),
    "horizontal-slot-frame": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_horizontal-slot-frame.png'),
    "vertical-slot-frame": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_vertical-slot-frame.png'),
    "empty-item-slot": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_empty-item-slot.png'),
    "separation-frame": os.path.join(PATTERNS_DIR_PATH, f'eq_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_separation-frame.png'),
}

chest_inventory_patterns_paths = {
    "chest-small": os.path.join(PATTERNS_DIR_PATH, f'chest_small_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
    "chest-big": os.path.join(PATTERNS_DIR_PATH, f'chest_big_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
    "chest-small_mask": os.path.join(PATTERNS_DIR_PATH, f'chest_small_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png'),
    "chest-big_mask": os.path.join(PATTERNS_DIR_PATH, f'chest_big_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png'),
    "bottom-frame": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bottom-frame.png'),
    "left-frame": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_left-frame.png'),
    "horizontal-slot-frame": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_horizontal-slot-frame.png'),
    "vertical-slot-frame": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_vertical-slot-frame.png'),
    "empty-item-slot": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_empty-item-slot.png'),
    "separation-frame_1": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_separation-frame_1.png'),
    "separation-frame_2": os.path.join(PATTERNS_DIR_PATH, f'chest_inventory_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_separation-frame_2.png'),
}

items_quantity_pattern = os.path.join(PATTERNS_DIR_PATH, f'item_quantity_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')

items_patterns_paths = {
    "coal": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_coal_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_coal_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "copper-ore": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_copper-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_copper-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "diamond": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_diamond_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_diamond_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "emerald": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_emerald_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_emerald_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "glowstone-dust": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_glowstone-dust_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_glowstone-dust_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "gold-nugget": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_gold-nugget_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_gold-nugget_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "gold-ore": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_gold-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_gold-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "iron-ingot": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_iron-ingot_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_iron-ingot_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "iron-nugget": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_iron-nugget_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_iron-nugget_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "iron-ore": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_iron-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_iron-ore_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "lapis-lazuli": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_lapis-lazuli_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_lapis-lazuli_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "nether-quartz": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_nether-quartz_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_nether-quartz_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "redstone-dust": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_redstone-dust_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_redstone-dust_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "stone": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_stone_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_stone_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "cobblestone": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_cobblestone_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_cobblestone_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
}

item_destruction_patterns_paths = {
        0: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_0_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        1: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_1_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        2: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_2_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        3: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_3_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        4: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_4_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        5: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_5_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        6: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_6_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        7: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_7_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        8: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_8_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        9: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_9_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        10: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_10_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        11: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_11_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        12: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_12_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        13: {
            "bar_path": os.path.join(PATTERNS_DIR_PATH,
                                     f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_13_bar.png'),
            "bar_mask_path": os.path.join(PATTERNS_DIR_PATH,
                                          f'item_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_bar_mask.png'),
        },
        14: {
            "bar_path": None,
            "bar_mask_path": None,
        }
    }

def get_config_dict():
    """
    Creates and returns a configuration dictionary based on the current settings.

    This function compiles various configuration settings into a dictionary. These settings include command paths, hotkeys, and other parameters relevant to the application's operation.

    Returns:
        dict: A dictionary containing various configuration settings.
    """
    tmp_dict = {}
    # tmp_dict["pattern_settings"] = pattern_settings
    tmp_dict["homes"] = {
        "repair": command_home_repair,
        "mining": command_home_mining,
        "chest": command_home_chest,
        "farm": command_home_farm,
        "tmp": command_home_tmp,
    }
    tmp_dict["sell_inventory_command"] = command_sell_inventory
    tmp_dict["autoclicker_delay_ms"] = autoclicker_delay_ms
    tmp_dict["afk_breaks"] = afk_breaks_flag
    tmp_dict["farm_floors_number"] = farm_floors_number
    tmp_dict["farm_floor_time_moving"] = farm_floor_time_moving
    tmp_dict["game_hotkeys"] = {
        "esc": hotkey_esc,
        "enter": hotkey_enter,
        "chat": hotkey_chat,
        "inventory": hotkey_inventory,
        "moving_up": hotkey_moving_up,
        "moving_down": hotkey_moving_down,
        "moving_left": hotkey_moving_left,
        "moving_right": hotkey_moving_right,
    }
    tmp_dict["app_buttons"] = {
        "autoclicker_lpm": button_autoclicker_lpm,
        "autoclicker_ppm": button_autoclicker_ppm,
        "mine": button_mine_procedure,
        "farm": button_farm_procedure,
    }
    tmp_dict["protected_slots"] = list(protected_slots)
    tmp_dict["items_stored_list"] = items_stored_list
    tmp_dict["eq_limit_to_stored"] = eq_limit_to_stored
    tmp_dict["mine_moving_time"] = moving_time
    tmp_dict["mine_moving_hold_shift"] = moving_hold_shift
    tmp_dict["chat_messages_flag"] = chat_messages_flag
    tmp_dict["chat_messages_list"] = chat_messages
    tmp_dict["chat_messages_frequency_min"] = chat_messages_frequency_min
    tmp_dict["tmp_home_flag"] = tmp_home_flag
    return tmp_dict

def set_config_from_dict(config_dict):
    """
    Sets the global configuration based on the provided dictionary.

    This function updates the global configuration variables with the values provided in the config_dict.
    It affects various aspects of the application, including commands, hotkeys, and operational parameters.

    Args:
        config_dict (dict): A dictionary containing configuration settings to be applied.

    Note:
        If a particular configuration setting is not present in the provided dictionary, it retains its previous value. If the provided dictionary is None, no changes are made to the configuration.
    """
    global pattern_settings
    global command_home_repair
    global command_home_mining
    global command_home_chest
    global command_home_farm
    global command_home_tmp
    global command_sell_inventory
    global autoclicker_delay_ms
    global afk_breaks_flag
    global farm_floors_number
    global farm_floor_time_moving
    global hotkey_esc
    global hotkey_enter
    global hotkey_chat
    global hotkey_inventory
    global hotkey_moving_up
    global hotkey_moving_down
    global hotkey_moving_left
    global hotkey_moving_right
    global button_autoclicker_lpm
    global button_autoclicker_ppm
    global button_mine_procedure
    global button_farm_procedure
    global protected_slots
    global items_stored_list
    global eq_limit_to_stored
    global moving_time
    global moving_hold_shift
    global chat_messages_flag
    global chat_messages
    global chat_messages_frequency_min
    global tmp_home_flag
    if config_dict is not None:
        # if "pattern_settings" in config_dict:
        #     pattern_settings = config_dict["pattern_settings"]
        if "homes" in config_dict:
            command_home_repair = config_dict["homes"]["repair"]
            command_home_mining = config_dict["homes"]["mining"]
            command_home_chest = config_dict["homes"]["chest"]
            command_home_farm = config_dict["homes"]["farm"]
            command_home_tmp = config_dict["homes"]["tmp"]
        if "sell_inventory_command" in config_dict:
            command_sell_inventory = config_dict["sell_inventory_command"]
        if "autoclicker_delay_ms" in config_dict:
            autoclicker_delay_ms = config_dict["autoclicker_delay_ms"]
        if "afk_breaks" in config_dict:
            afk_breaks_flag = config_dict["afk_breaks"]
        if "farm_floors_number" in config_dict:
            farm_floors_number = config_dict["farm_floors_number"]
        if "farm_floor_time_moving" in config_dict:
            farm_floor_time_moving = config_dict["farm_floor_time_moving"]
        if "game_hotkeys" in config_dict:
            hotkey_esc = config_dict["game_hotkeys"]["esc"]
            hotkey_enter = config_dict["game_hotkeys"]["enter"]
            hotkey_chat = config_dict["game_hotkeys"]["chat"]
            hotkey_inventory = config_dict["game_hotkeys"]["inventory"]
            hotkey_moving_up = config_dict["game_hotkeys"]["moving_up"]
            hotkey_moving_down = config_dict["game_hotkeys"]["moving_down"]
            hotkey_moving_left = config_dict["game_hotkeys"]["moving_left"]
            hotkey_moving_right = config_dict["game_hotkeys"]["moving_right"]
        if "app_buttons" in config_dict:
            button_autoclicker_lpm = config_dict["app_buttons"]["autoclicker_lpm"]
            button_autoclicker_ppm = config_dict["app_buttons"]["autoclicker_ppm"]
            button_mine_procedure = config_dict["app_buttons"]["mine"]
            button_farm_procedure = config_dict["app_buttons"]["farm"]
        if "protected_slots" in config_dict:
            protected_slots = set(config_dict["protected_slots"])
        if "items_stored_list" in config_dict:
            items_stored_list = config_dict["items_stored_list"]
        if "eq_limit_to_stored" in config_dict:
            eq_limit_to_stored = config_dict["eq_limit_to_stored"]
        if "mine_moving_time" in config_dict:
            moving_time = config_dict["mine_moving_time"]
        if "mine_moving_hold_shift" in config_dict:
            moving_hold_shift = config_dict["mine_moving_hold_shift"]
        if "chat_messages_flag" in config_dict:
            chat_messages_flag = config_dict["chat_messages_flag"]
        if "chat_messages_list" in config_dict:
            chat_messages = config_dict["chat_messages_list"]
        if "chat_messages_frequency_min" in config_dict:
            chat_messages_frequency_min = config_dict["chat_messages_frequency_min"]
        if "tmp_home_flag" in config_dict:
            tmp_home_flag = config_dict["tmp_home_flag"]
        app_logger.info(f"The configuration was loaded: {config_dict}")
    else:
        app_logger.info(f"Taked config dict is None")

comments = {
    # 'pattern_settings': f"# pattern_settings - Settings for the patterns used by the application. \n# Note: patterns must be in the 'patterns' directory \n#     'width': - determines the width of the game window for which the used patterns were prepared, default value '{pattern_settings['width']}'. \n#     'height' - determines the height of the game window for which the used patterns were prepared, default value '{pattern_settings['height']}'. \n#     'texture_pack' - determines the game texturepack used in patterns, default value '{pattern_settings['texture_pack']}' \n#     'eq_size' - determines the game settings which represent the used patterning (game: options -> Video Settings -> GUI Scale), default value '{pattern_settings['eq_size']}'. \n",
    'homes': f"# homes - Teleport command settings to key locations used in the scrip. \n#      'repair' - location used for repairing tools, default value '{command_home_repair}'. \n#      'mining' - location of mining, default value '{command_home_mining}' \n#      'chest' - location of the chest for depositing items, default value '{command_home_chest}'. \n#      'farm' - farm location prefix, default value '{command_home_farm}' \n#      'tmp' - tmp location prefix, default value '{command_home_farm}' \n",
    'sell_inventory_command': f"# sell_inventory_command - Command to sell items, default value '{command_sell_inventory}' \n",
    'autoclicker_delay_ms': f"# autoclicker_delay_ms - Frequency used in autoclicker, default value '{autoclicker_delay_ms}' \n",
    'afk_breaks': f"# afk_breaks - True or False flag specifying whether random interrupts are to be used, default value '{afk_breaks_flag}' \n",
    'farm_floors_number': f"# farm_floors_number - Number of floors handled by the farm bot, default value '{farm_floors_number}' \n",
    'farm_floor_time_moving': f"# farm_floor_time_moving - Time for the farm bot to move in a certain direction, default value '{farm_floor_time_moving}' \n",
    'game_hotkeys': f"# game_hotkeys - Setting ID hotkeys game settings \n#     'esc' - hotkey to close the window default value '{hotkey_esc}' \n#     'enter' - hotkey to send a message default value '{hotkey_enter}' \n#     'chat' - hotkey to open chat default value '{hotkey_chat}' \n#     'inventory' - hotkey to open and close the inventory default value '{hotkey_inventory}' \n#     'moving_up' - hotkey of moving forward default value '{hotkey_moving_up}' \n#     'moving_down' - hotkey moving backwards default value '{hotkey_moving_down}' \n#     'moving_left' - hotkey moving left default value '{hotkey_moving_left}' \n#     'moving_right' - hotkey moving to the right default value '{hotkey_moving_right}' \n",
    'app_buttons': f"# app_buttons - Application management button settings \n#     'autoclicker_lpm' - setting the ID of the button that turns the left mouse button autoclicker on and off, default value '{button_autoclicker_lpm}' \n#     'autoclicker_ppm' - setting the ID of the right mouse button autoclicker on and off button, default value '{button_autoclicker_ppm} \n#     'mine' - setting the ID of the button to enable and disable the autoclicker procedure, default value '{button_mine_procedure} \n#     'farm' - setting the ID of the button that turns the autofarm procedure on and off, default value '{button_farm_procedure} \n",
    'protected_slots': f"# protected_slots - A collection of slots protected from being put away in a box, default value '{protected_slots}' \n",
    'items_stored_list': f"# items_stored_list - list of items stored in the chest before sale, default value '{items_stored_list}' \n",
    'eq_limit_to_stored': f"# eq_limit_to_stored - Determines the number of slots that start the procedure of putting items in the chest, default value '{eq_limit_to_stored}' \n",
    'mine_moving_time': f"# mine_moving_time - Time for the mine bot to move in a certain direction, default value '{moving_time}' \n",
    'mine_moving_hold_shift': f"# mine_moving_hold_shift - True or False flag specifying pressing the 'shift' button during the digging procedure, default value '{moving_hold_shift}' \n",
    'chat_messages_flag': f"# chat_messages_flag - True or False flag to specify sending messages to the chat, default value '{chat_messages_flag} \n",
    'chat_messages_list': f"# chat_messages_list - List of messages sent to the chat \n",
    'chat_messages_frequency_min': f"# chat_messages_frequency_min - Frequency of sending chat messages, default value '{chat_messages_frequency_min}' \n",
    'tmp_home_flag': f"# tmp_home_flag - A value of True or False, determines whether the program should use set and go home temporary, default value '{tmp_home_flag}' \n",
}

def encode_special_characters(string: str) -> str:
    """
    Encodes special characters in a string using URL encoding.

    This function is used to encode special characters in strings that need to be saved in a YAML file, preventing formatting issues.

    Args:
        string (str): The string to encode.

    Returns:
        str: The encoded string.
    """
    return urllib.parse.quote(string, safe='')

def decode_special_characters(string: str) -> str:
    """
    Decodes special characters from a URL-encoded string.

    This function reverses the encoding done by 'encode_special_characters' function, returning the original string.

    Args:
        string (str): The URL-encoded string to decode.

    Returns:
        str: The decoded original string.
    """
    return urllib.parse.unquote(string)


def save_config_dict(config_dict: Dict[str, any]) -> None:
    """
    Saves the configuration dictionary to a YAML file with added comments.

    This function encodes special characters in specific keys, converts the dictionary to YAML format, and adds predefined comments to the YAML file before saving it.

    Args:
        config_dict (dict): The configuration dictionary to save.
    """
    try:
        for key in ['chat_messages', 'sell_inventory_command']:
            if key in config_dict:
                value = config_dict[key]
                if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
                    config_dict[key] = encode_special_characters(value[0])
        yaml_str = yaml.dump(config_dict, allow_unicode=True, default_flow_style=False)
        yaml_with_comments = ""
        for line in yaml_str.splitlines():
            key = line.split(":")[0].strip()
            comment = comments.get(key, '')
            yaml_with_comments += comment + line + '\n'
        yaml_with_comments = "# APP CONFIG: \n" + yaml_with_comments
        with open(config_file_path, 'w', encoding='utf-8') as file:
            file.write(yaml_with_comments)
        app_logger.info("Configuration file has been saved")
    except Exception as ex:
        app_logger.error(ex)

def read_config_file() -> Dict[str, any]:
    """
    Reads the configuration from a YAML file and returns it as a dictionary.

    This function decodes special characters in specific keys and converts the YAML file content back to a dictionary format.

    Returns:
        dict: The configuration dictionary read from the file.
    """
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        for key in ['chat_messages', 'sell_inventory_command']:
            if key in config:
                if isinstance(config[key], str):
                    config[key] = decode_special_characters(config[key])
                elif isinstance(config[key], list):
                    config[key] = [decode_special_characters(item) if isinstance(item, str) else item for item in config[key]]
        app_logger.debug(f"config from path: {config_file_path} was readed.")
        return config
    except Exception as ex:
        app_logger.error(ex)

def setup_config_file() -> None:
    """
    Sets up the configuration file for the application.

    This function checks if the configuration file exists, creates it if it doesn't,
    reads the existing configuration, and updates it based on the current settings.
    """
    try:
        if not os.path.exists(config_file_path):
            save_config_dict(get_config_dict())
            app_logger.info("The configuration file does not exist, a configuration file has been created.")
        config = read_config_file()
        set_config_from_dict(config)
        save_config_dict(get_config_dict())
    except Exception as ex:
        app_logger.error(ex)
