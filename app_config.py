import os
from typing import Dict, Set, List
import yaml
import urllib.parse
from logger import app_logger

APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR_PATH = os.path.join(APP_PATH, 'outputs')
PATTERNS_DIR_PATH = os.path.join(APP_PATH, 'patterns')

game_window_name = 'Minecraft'

save_images_flags = {
    "find_chest_big_pattern": False,
    "get_chest_big_image": False,
    "find_chest_small_pattern": False,
    "get_chest_small_image": False,
    "check_and_get_chest_image": False,
    "get_slots_chest_coordinates": False,
    "get_chest_slots_images": False,
    "find_item_pattern_in_item_image": False,
    "extract_text_from_image": False,
}

game_latest_log_path = os.path.join('C:', os.sep, 'Users', 'Artur', 'AppData', 'Roaming', '.minecraft', 'logs', 'latest.log')

def get_game_latest_log_path() -> str:
    return game_latest_log_path

coordinates_screen_XYZ = {
    "x1": 11,
    "y1": 304,
    "x2": 600,
    "y2": 331,
}

def get_coordinates_screen_XYZ() -> dict:
    return coordinates_screen_XYZ

coordinates_screen_XYZ_analysis_flag = True

def get_coordinates_screen_XYZ_analysis_flag() -> bool:
    return coordinates_screen_XYZ_analysis_flag

coordinates_screen_Facing = {
    "x1": 11,
    "y1": 385,
    "x2": 800,
    "y2": 412,
}

def get_coordinates_screen_Facing() -> dict:
    return coordinates_screen_Facing

mine_coordinate_range = {
    'x1': 0,
    'x2': 0,
    'y1': 0,
    'y2': 0,
    'z1': 0,
    'z2': 0,
}

def get_mine_coordinate_range() -> dict:
    return mine_coordinate_range

farm_coordinate_range = [
{
    'x1': 0,
    'x2': 0,
    'y1': 0,
    'y2': 0,
    'z1': 0,
    'z2': 0,
},
{
    'x1': 0,
    'x2': 0,
    'y1': 0,
    'y2': 0,
    'z1': 0,
    'z2': 0,
}
]

def get_farm_coordinate_range() -> list:
    return farm_coordinate_range

grinder_coordinate_range = {
    'x1': 0,
    'x2': 0,
    'y1': 0,
    'y2': 0,
    'z1': 0,
    'z2': 0,
}

def get_grinder_coordinate_range() -> dict:
    return grinder_coordinate_range

coordinates_problem_messages_list = [
    "aha?",
    "?",
    "xd",
    "xd?"
]

def get_coordinates_problem_messages_list() -> list:
    return coordinates_problem_messages_list

client_player_nickname = ""

def get_client_player_nickname() -> str:
    return client_player_nickname

risk_nicks_list = [
    "Artur",
]

def get_risk_nicks_list() -> list:
    return risk_nicks_list

reply_all_nicks_flag = False

def get_reply_all_nicks_flag() -> bool:
    return reply_all_nicks_flag

def get_save_images_flags() -> dict:
    return save_images_flags

def get_game_window_name() -> str:
    return game_window_name

messages_respond_dict = {
    '.': '?',
    '?': '?',
    'halo': 'Co tam?',
    'zyjesz': '?',
    'Artur': '?',
}
def get_messages_respond_dict() -> dict:
    return messages_respond_dict

chat_message_answer_flag = False

def get_chat_message_answer_flag() -> bool:
    return chat_message_answer_flag

private_message_answer_flag = True

def get_private_message_answer_flag() -> bool:
    return private_message_answer_flag

counter_risk_messages_to_afk = 0

def get_counter_risk_messages_to_afk() -> int:
    return counter_risk_messages_to_afk

counter_risk_messages_to_lobby = 0

def get_counter_risk_messages_to_lobby() -> int:
    return counter_risk_messages_to_lobby

config_file_path = os.path.join(APP_PATH, 'config.yaml')

def get_config_file_path() -> str:
    return config_file_path

command_spawn = '/spawn'
command_home_repair = '/home repair'
command_home_mining = '/home mine'
command_home_chest = '/home chest'
command_home_farm = '/home farm'
command_home_grinder = '/home mobgrinder'
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

def get_command_home_grinder() -> str:
    return command_home_grinder

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

# pickaxe_pattern_path = os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full.png')
pickaxe_patterns_paths = {
    "diamond": os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_diamond.png'),
    "enchanted-diamond": os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-diamond.png'),
    "netherite": os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_netherite.png'),
    "enchanted-netherite": os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-netherite.png'),
}
pickaxe_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'pickaxe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_mask.png')

# axe_pattern_path = os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full.png')
axe_patterns_paths = {
    "diamond": os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_diamond.png'),
    "enchanted-diamond": os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-diamond.png'),
    "netherite": os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_netherite.png'),
    "enchanted-netherite": os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-netherite.png'),
}
axe_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'axe_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_mask.png')

sword_patterns_paths = {
    "diamond": os.path.join(PATTERNS_DIR_PATH, f'sword_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_diamond.png'),
    "enchanted-diamond": os.path.join(PATTERNS_DIR_PATH, f'sword_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-diamond.png'),
    "netherite": os.path.join(PATTERNS_DIR_PATH, f'sword_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_netherite.png'),
    "enchanted-netherite": os.path.join(PATTERNS_DIR_PATH, f'sword_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_enchanted-netherite.png'),
}
sword_pattern_mask_path = os.path.join(PATTERNS_DIR_PATH, f'sword_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_full_mask.png')

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
farm_sell_frequency = 0
farm_store_items = False

tmp_home_flag = True

def get_farm_number() -> int:
    return farm_number

def get_farm_floors_number() -> int:
    return farm_floors_number

def get_farm_floor_time_moving() -> int:
    return farm_floor_time_moving

def get_farm_sell_frequency() -> int:
    return farm_sell_frequency

def get_farm_store_items() -> int:
    return farm_store_items

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

button_stop = 74
button_autoclicker_lpm = 79
button_autoclicker_ppm = 80
button_mine_procedure = 78
button_farm_procedure = 69
button_mobgrinder_procedure = 55

def get_button_stop() -> int:
    return button_stop

def get_button_autoclicker_lpm() -> int:
    return button_autoclicker_lpm

def get_button_autoclicker_ppm() -> int:
    return button_autoclicker_ppm

def get_button_mine_procedure() -> int:
    return button_mine_procedure

def get_button_farm_procedure() -> int:
    return button_farm_procedure

def get_button_mobgrinder_procedure() -> int:
    return button_mobgrinder_procedure

protected_slots = set([7,8,9])

def get_protected_slots():
    return protected_slots

def set_protected_slots(new_protected_slots: Set[int]) -> None:
    app_logger.debug(f"set_protected_slots() - new_protected_slots: {new_protected_slots}")
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

items_stored_list = ["diamond", "emerald", "gold-ore", "iron-ingot", "iron-ore", "diamond-block"]

def get_items_stored_list():
    return items_stored_list

def set_items_stored_list(new_items_stored_list: List[str]) -> None:
    app_logger.debug(f"set_items_stored_list() - new_items_stored_list: {new_items_stored_list}")
    global items_stored_list
    items_stored_list = new_items_stored_list

chat_messages_flag = True
chat_messages = ['&2&lUWAGA! &f&lKupię &6&lGąbki &7- &e&l100&6&l$ &f&lza sztukę! &a&l(2,9k za 29 sztuk / 6,4k za stack) &7- &b&l/msg &7- &f&lNie ma mnie? Nie odpisuję? Napisz do innego członka &7[&b&lS&f&lB&7&l-&f&lM&b&laf&9&lia&7]']
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
    "diamond-block": {
        "pattern": os.path.join(PATTERNS_DIR_PATH, f'item_diamond-block_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH, f'item_diamond-block_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
    },
    "gunpowder": {
        "pattern": os.path.join(PATTERNS_DIR_PATH,
                                f'item_gunpowder_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}.png'),
        "mask": os.path.join(PATTERNS_DIR_PATH,
                             f'item_gunpowder_{pattern_settings["texture_pack"]}_EQ{pattern_settings["eq_size"]}_{pattern_settings["width"]}x{pattern_settings["height"]}_mask.png')
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
        "mobgrinder": command_home_grinder,
        "tmp": command_home_tmp,
    }
    tmp_dict["sell_inventory_command"] = command_sell_inventory
    tmp_dict["autoclicker_delay_ms"] = autoclicker_delay_ms
    tmp_dict["afk_breaks"] = afk_breaks_flag
    tmp_dict["farm_number"] = farm_number
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
        "button_stop": button_stop,
        "autoclicker_lpm": button_autoclicker_lpm,
        "autoclicker_ppm": button_autoclicker_ppm,
        "mine": button_mine_procedure,
        "farm": button_farm_procedure,
        "mobgrinder": button_mobgrinder_procedure,
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
    tmp_dict["game_latest_log_path"] = game_latest_log_path
    tmp_dict["risk_nicks_list"] = risk_nicks_list
    tmp_dict["messages_respond_dict"] = messages_respond_dict
    tmp_dict["chat_message_answer_flag"] = chat_message_answer_flag
    tmp_dict["private_message_answer_flag"] = private_message_answer_flag
    tmp_dict["counter_risk_messages_to_afk"] = counter_risk_messages_to_afk
    tmp_dict["counter_risk_messages_to_lobby"] = counter_risk_messages_to_lobby
    tmp_dict["farm_sell_frequency"] = farm_sell_frequency
    tmp_dict["farm_store_items"] = farm_store_items
    tmp_dict["reply_all_nicks_flag"] = reply_all_nicks_flag
    tmp_dict["coordinates_screen_XYZ"] = coordinates_screen_XYZ
    tmp_dict["coordinates_screen_Facing"] = coordinates_screen_Facing
    tmp_dict["mine_coordinate_range"] = mine_coordinate_range
    tmp_dict["farm_coordinate_range"] = farm_coordinate_range
    tmp_dict["grinder_coordinate_range"] = grinder_coordinate_range
    tmp_dict["coordinates_problem_messages_list"] = coordinates_problem_messages_list
    return tmp_dict

def set_config_from_dict(config_dict: dict) -> None:
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
    global command_home_grinder
    global command_home_tmp
    global command_sell_inventory
    global autoclicker_delay_ms
    global afk_breaks_flag
    global farm_number
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
    global button_stop
    global button_autoclicker_lpm
    global button_autoclicker_ppm
    global button_mine_procedure
    global button_farm_procedure
    global button_mobgrinder_procedure
    global protected_slots
    global items_stored_list
    global eq_limit_to_stored
    global moving_time
    global moving_hold_shift
    global chat_messages_flag
    global chat_messages
    global chat_messages_frequency_min
    global tmp_home_flag
    global game_latest_log_path
    global risk_nicks_list
    global messages_respond_dict
    global chat_message_answer_flag
    global private_message_answer_flag
    global client_player_nickname
    global counter_risk_messages_to_afk
    global counter_risk_messages_to_lobby
    global farm_sell_frequency
    global farm_store_items
    global reply_all_nicks_flag
    global coordinates_screen_XYZ
    global coordinates_screen_Facing
    global mine_coordinate_range
    global farm_coordinate_range
    global grinder_coordinate_range
    global coordinates_problem_messages_list
    if config_dict is not None:
        # if "pattern_settings" in config_dict:
        #     pattern_settings = config_dict["pattern_settings"]
        if "homes" in config_dict:
            command_home_repair = config_dict["homes"]["repair"]
            command_home_mining = config_dict["homes"]["mining"]
            command_home_chest = config_dict["homes"]["chest"]
            command_home_farm = config_dict["homes"]["farm"]
            command_home_grinder = config_dict["homes"]["mobgrinder"]
            command_home_tmp = config_dict["homes"]["tmp"]
        if "sell_inventory_command" in config_dict:
            command_sell_inventory = config_dict["sell_inventory_command"]
        if "autoclicker_delay_ms" in config_dict:
            autoclicker_delay_ms = config_dict["autoclicker_delay_ms"]
        if "afk_breaks" in config_dict:
            afk_breaks_flag = config_dict["afk_breaks"]
        if "farm_number" in config_dict:
            farm_number = config_dict["farm_number"]
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
            button_stop = config_dict["app_buttons"]["button_stop"]
            button_autoclicker_lpm = config_dict["app_buttons"]["autoclicker_lpm"]
            button_autoclicker_ppm = config_dict["app_buttons"]["autoclicker_ppm"]
            button_mine_procedure = config_dict["app_buttons"]["mine"]
            button_farm_procedure = config_dict["app_buttons"]["farm"]
            button_mobgrinder_procedure = config_dict["app_buttons"]["mobgrinder"]
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
        if "game_latest_log_path" in config_dict:
            game_latest_log_path = config_dict["game_latest_log_path"]
        if "risk_nicks_list" in config_dict:
            risk_nicks_list = config_dict["risk_nicks_list"]
        if "messages_respond_dict" in config_dict:
            messages_respond_dict = config_dict["messages_respond_dict"]
        if "chat_message_answer_flag" in config_dict:
            chat_message_answer_flag = config_dict["chat_message_answer_flag"]
        if "private_message_answer_flag" in config_dict:
            private_message_answer_flag = config_dict["private_message_answer_flag"]
        if "client_player_nickname" in config_dict:
            client_player_nickname = config_dict["client_player_nickname"]
        if "counter_risk_messages_to_afk" in config_dict:
            counter_risk_messages_to_afk = config_dict["counter_risk_messages_to_afk"]
        if "counter_risk_messages_to_lobby" in config_dict:
            counter_risk_messages_to_lobby = config_dict["counter_risk_messages_to_lobby"]
        if "farm_sell_frequency" in config_dict:
            farm_sell_frequency = config_dict["farm_sell_frequency"]
        if "farm_store_items" in config_dict:
            farm_store_items = config_dict["farm_store_items"]
        if "reply_all_nicks_flag" in config_dict:
            reply_all_nicks_flag = config_dict["reply_all_nicks_flag"]
        if "coordinates_screen_XYZ" in config_dict:
            coordinates_screen_XYZ = config_dict["coordinates_screen_XYZ"]
        if "coordinates_screen_Facing" in config_dict:
            coordinates_screen_Facing = config_dict["coordinates_screen_Facing"]
        if "mine_coordinate_range" in config_dict:
            mine_coordinate_range = config_dict["mine_coordinate_range"]
        if "farm_coordinate_range" in config_dict:
            farm_coordinate_range = config_dict["farm_coordinate_range"]
        if "coordinates_problem_messages_list" in config_dict:
            coordinates_problem_messages_list = config_dict["coordinates_problem_messages_list"]
        if "grinder_coordinate_range" in config_dict:
            grinder_coordinate_range = config_dict["grinder_coordinate_range"]
        app_logger.info(f"The configuration was loaded: {config_dict}")
    else:
        app_logger.info(f"Taked config dict is None")

comments = {
    # 'pattern_settings': f"# pattern_settings - Settings for the patterns used by the application. \n# Note: patterns must be in the 'patterns' directory \n#     'width': - determines the width of the game window for which the used patterns were prepared, default value '{pattern_settings['width']}'. \n#     'height' - determines the height of the game window for which the used patterns were prepared, default value '{pattern_settings['height']}'. \n#     'texture_pack' - determines the game texturepack used in patterns, default value '{pattern_settings['texture_pack']}' \n#     'eq_size' - determines the game settings which represent the used patterning (game: options -> Video Settings -> GUI Scale), default value '{pattern_settings['eq_size']}'. \n",
    'homes': f"# homes - Teleport command settings to key locations used in the scrip. \n#      'repair' - location used for repairing tools, default value '{command_home_repair}'. \n#      'mining' - location of mining, default value '{command_home_mining}' \n#      'chest' - location of the chest for depositing items, default value '{command_home_chest}' \n#      'farm' - farm location prefix, default value '{command_home_farm}' \n#      'mobgrinder' - mobgrinder location prefix, default value '{command_home_grinder}' \n#      'tmp' - tmp location prefix, default value '{command_home_farm}' \n",
    'sell_inventory_command': f"# sell_inventory_command - Command to sell items, default value '{command_sell_inventory}' \n",
    'autoclicker_delay_ms': f"# autoclicker_delay_ms - Frequency used in autoclicker, default value '{autoclicker_delay_ms}' \n",
    'afk_breaks': f"# afk_breaks - True or False flag specifying whether random interrupts are to be used, default value '{afk_breaks_flag}' \n",
    'farm_number': f"# farm_number - Number of farms used by the farm bot, default value '{farm_number}' \n",
    'farm_floors_number': f"# farm_floors_number - Number of floors handled by the farm bot, default value '{farm_floors_number}' \n",
    'farm_floor_time_moving': f"# farm_floor_time_moving - Time for the farm bot to move in a certain direction, default value '{farm_floor_time_moving}' \n",
    'game_hotkeys': f"# game_hotkeys - Setting ID hotkeys game settings \n#     'esc' - hotkey to close the window default value '{hotkey_esc}' \n#     'enter' - hotkey to send a message default value '{hotkey_enter}' \n#     'chat' - hotkey to open chat default value '{hotkey_chat}' \n#     'inventory' - hotkey to open and close the inventory default value '{hotkey_inventory}' \n#     'moving_up' - hotkey of moving forward default value '{hotkey_moving_up}' \n#     'moving_down' - hotkey moving backwards default value '{hotkey_moving_down}' \n#     'moving_left' - hotkey moving left default value '{hotkey_moving_left}' \n#     'moving_right' - hotkey moving to the right default value '{hotkey_moving_right}' \n",
    'app_buttons': f"# app_buttons - Application management button settings \n#     'button_stop' - setting a button ID that completely disables the application, default value '{button_stop}' \n#     'autoclicker_lpm' - setting the ID of the button that turns the left mouse button autoclicker on and off, default value '{button_autoclicker_lpm}' \n#     'autoclicker_ppm' - setting the ID of the right mouse button autoclicker on and off button, default value '{button_autoclicker_ppm} \n#     'mine' - setting the ID of the button to enable and disable the autoclicker procedure, default value '{button_mine_procedure} \n#     'farm' - setting the ID of the button that turns the autofarm procedure on and off, default value '{button_farm_procedure} \n#     'mobgrinder' - setting the ID of the button that turns the mobgrinder procedure on and off, default value '{button_mobgrinder_procedure} \n",
    'protected_slots': f"# protected_slots - A collection of slots protected from being put away in a box, default value '{protected_slots}' \n",
    'items_stored_list': f"# items_stored_list - list of items stored in the chest before sale, default value '{items_stored_list}' \n",
    'eq_limit_to_stored': f"# eq_limit_to_stored - Determines the number of slots that start the procedure of putting items in the chest, default value '{eq_limit_to_stored}' \n",
    'mine_moving_time': f"# mine_moving_time - Time for the mine bot to move in a certain direction, default value '{moving_time}' \n",
    'mine_moving_hold_shift': f"# mine_moving_hold_shift - True or False flag specifying pressing the 'shift' button during the digging procedure, default value '{moving_hold_shift}' \n",
    'chat_messages_flag': f"# chat_messages_flag - True or False flag to specify sending messages to the chat, default value '{chat_messages_flag} \n",
    'chat_messages_list': f"# chat_messages_list - List of messages sent to the chat \n",
    'chat_messages_frequency_min': f"# chat_messages_frequency_min - Frequency of sending chat messages, default value '{chat_messages_frequency_min}' \n",
    'tmp_home_flag': f"# tmp_home_flag - A value of True or False, determines whether the program should use set and go home temporary, default value '{tmp_home_flag}' \n",
    'game_latest_log_path': f"# game_latest_log_path - Path of the last log file that is changed by the game in real time (required to analyze chat text messages), default value '{game_latest_log_path}' \n",
    'risk_nicks_list': f"# risk_nicks_list - List of nicks that are a threat (usually a list of administration) from which messages are analyzed and appropriate actions are performed according to the configuration., default value '{risk_nicks_list}' \n",
    'messages_respond_dict': f"# messages_respond_dict - Response dictionary used to reply to messages of people on the list of endangered nicknames: The first value is the content of the message received from the sender, the second value is the content of the reply. The default value for content from outside the dictionary is: '?', default value '{messages_respond_dict}' \n",
    'chat_message_answer_flag': f"# chat_message_answer_flag - Flag on whether the program should respond to messages appearing in the public chat directed to the set nickname., default value '{chat_message_answer_flag}' \n",
    'private_message_answer_flag': f"# private_message_answer_flag - A flag regarding whether the program should respond to private messages that appear in the chat, default value '{private_message_answer_flag}' \n",
    'client_player_nickname': f"# client_player_nickname - Name (nick) of the player of the user using the program (needed to analyze public chat messages). NOTE: An empty string will make the program respond to every message of the person in the 'risk_nicks_list'. \n",
    'counter_risk_messages_to_afk': f"# counter_risk_messages_to_afk - Number of messages from risk nicks (from the risk_nicks_list) after which the program goes afk on the spawn, value 0 - no afk, default value '{counter_risk_messages_to_afk}\n",
    'counter_risk_messages_to_lobby': f"# counter_risk_messages_to_lobby - The number of messages from risk nicks (from the risk_nicks_list) after which the program exits to the lobby and completely stops the action, value 0 - no action execution, default value '{counter_risk_messages_to_lobby}\n",
    'farm_sell_frequency': f"# farm_sell_frequency - Determines the number of floors of the farm between sales (value <=0 will sell items on each floor), default value '{farm_sell_frequency}\n",
    'farm_store_items': f"# farm_store_items - A value of true or false declaring whether items are to be deposited into chests during autofarm (requires tmp and chest homes), default value '{farm_store_items}\n",
    'reply_all_nicks_flag': f"# reply_all_nicks_flag - True or False flag indicating whether the program should respond to messages from nicks outside the list (risk_nicks_list), default value '{reply_all_nicks_flag}\n",
    'coordinates_screen_XYZ': f"# coordinates_screen_XYZ - Coordinates on the screen of the XYZ field displayed on the screen after pressing 'F3' (USE show_config_coordinates.bat to show this coordinates), default value '{coordinates_screen_XYZ}\n",
    'coordinates_screen_Facing': f"# coordinates_screen_Facing - Coordinates on the screen of the Facing field displayed on the screen after pressing 'F3' (Note - the size of this field changes depending on the content) (USE show_config_coordinates.bat to show this coordinates), default value '{coordinates_screen_Facing}\n",
    'mine_coordinate_range': f"# mine_coordinate_range - Dict of the range of acceptable fla automine coordinates (for example, from x1=100 to x2=120). When any of the coordinates extracted from the analysis (coordinates_screen_XYZ) is out of range then the program aborts.\n",
    'farm_coordinate_range': f"# farm_coordinate_range - List containing dictionaries of the range of acceptable autofarm coordinates (for example, from y=-40 to y2=-20). When any of the coordinates extracted from the analysis (coordinates_screen_XYZ) is out of range then the program aborts.\n",
    'grinder_coordinate_range': f"# grinder_coordinate_range - Dict of the range of acceptable fla autogrinder coordinates (for example, from x1=-10 to x2=-12). When any of the coordinates extracted from the analysis (coordinates_screen_XYZ) is out of range then the program aborts.\n",
    'coordinates_problem_messages_list': f"# coordinates_problem_messages_list - List of messages that will be sent to the public chat in case of a problem with coordinates - an empty list will not send any message, default value '{coordinates_problem_messages_list}\n",
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
        app_logger.debug(f"config_dict to save: {config_dict}")
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
