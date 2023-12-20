import sys
import threading
import keyboard
import os
import pyautogui
from activities.chat import sellall_inventory
from activities.chest import update_chest_patterns_sizes
from activities.equipment import update_eq_patterns_sizes
from activities.farm import toggle_farm_procedure
from activities.mine import toggle_mine_procedure
from activities.mob_grinder import toggle_grinder_procedure
from app_config import OUTPUTS_DIR_PATH, PATTERNS_DIR_PATH, setup_config_file, get_button_mine_procedure, \
    get_button_farm_procedure, get_coordinates_screen_XYZ_analysis_flag, get_button_mobgrinder_procedure, \
    get_button_stop, get_hotkey_moving_left, get_hotkey_moving_right, get_hotkey_moving_up, get_hotkey_moving_down
from clicker import setup_autoclicer_hotkeys
from coordinate_analyzer import start_analyzer_XYZ_thread
from log_game_processor import start_messages_watcher_thread
from logger import app_logger
from patterns import load_patterns_all
from screenshooter import start_screenshot_thread
from typing import NoReturn

lock = threading.Lock()

def prepare_folders() -> None:
    """
    Creates necessary directories for the application if they do not exist.
    Specifically, it checks and creates the OUTPUTS_DIR_PATH and PATTERNS_DIR_PATH.
    """
    try:
        if not os.path.exists(OUTPUTS_DIR_PATH):
            os.makedirs(OUTPUTS_DIR_PATH)
            app_logger.debug(f"PATH: {OUTPUTS_DIR_PATH} do not exist, app create dir")
        if not os.path.exists(PATTERNS_DIR_PATH):
            os.makedirs(PATTERNS_DIR_PATH)
            app_logger.debug(f"PATH: {PATTERNS_DIR_PATH} do not exist, app create dir")
    except Exception as ex:
        app_logger.error(ex)

def sellall_inventory_thread() -> None:
    """
    Starts a new thread for selling inventory.
    This function sets the 'is_running_mine_procedure' flag to False and initiates the 'sellall_inventory' procedure in a separate thread.
    """
    global is_running_mine_procedure
    is_running_mine_procedure = False
    threading.Thread(target=sellall_inventory).start()
    app_logger.debug(f"Start sellall_inventory_thread")

def setup_buttons():
    """
    Sets up keyboard hotkeys for various application functionalities.
    Configures hotkeys for toggling mining and farming procedures, as well as autoclicker hotkeys.
    Additional hotkeys and their functions can be added as needed.
    """
    keyboard.add_hotkey(get_button_mine_procedure(), toggle_mine_procedure) #key '+' on numpad
    # keyboard.add_hotkey(71, repair_item_thread) #key '7' on numpad
    # keyboard.add_hotkey(72, sellall_inventory_thread) #key '8' on numpad
    keyboard.add_hotkey(get_button_farm_procedure(), toggle_farm_procedure) # key 'num lock' on numpad
    keyboard.add_hotkey(get_button_mobgrinder_procedure(), toggle_grinder_procedure) # key 'num lock' on numpad
    # keyboard.add_hotkey(82, test) # test key 'insert' on numpad
    setup_autoclicer_hotkeys()
    # keyboard.wait('esc')
    app_logger.debug(f"Setup buttons are done")

def stop_app() -> None:
    app_logger.debug(f"Release 'left'")
    pyautogui.mouseUp(button='left')
    app_logger.debug(f"Release 'shift'")
    keyboard.release('shift')
    app_logger.debug(f"Release {get_hotkey_moving_left()}")
    keyboard.release(get_hotkey_moving_left())
    app_logger.debug(f"Release {get_hotkey_moving_right()}")
    keyboard.release(get_hotkey_moving_right())
    app_logger.debug(f"Release {get_hotkey_moving_up()}")
    keyboard.release(get_hotkey_moving_up())
    app_logger.debug(f"Release {get_hotkey_moving_down()}")
    keyboard.release(get_hotkey_moving_down())
    app_logger.info(f"User stop app.")
    sys.exit(0)

def main() -> NoReturn:
    """
    Main function to initiate the application.
    Performs initial setup including loading configuration, preparing folders, loading patterns, updating sizes, setting up buttons, and starting the screenshot thread.
    Waits for a specific keypress ('-' on numpad) to stop the application.
    Logs the start and stop of the application.
    """
    # TODO: dodać zabezpieczenia aby aplikacja wykonywała czynności tylko gdy okno gry jest aktywne (ma focus)
    # TODO: dodanie procedury która sprawi, że okno będzie aktywne oraz zmieni cztery razy tryb okna gry klikajac f11 -  problem występuje przy trybie pełnoekranowym oraz alt+tab
    setup_config_file()
    prepare_folders()
    load_patterns_all()
    update_eq_patterns_sizes()
    update_chest_patterns_sizes()
    setup_buttons()
    start_screenshot_thread()
    start_messages_watcher_thread()
    if get_coordinates_screen_XYZ_analysis_flag():
        start_analyzer_XYZ_thread()

    print("Application started.")
    app_logger.info(f"Application started")
    print("Press '+' on numpad to start mine procedure.")
    print("Press '-' on numpad to stop app.")

    keyboard.wait(get_button_stop())  # test key '-' on numpad
    stop_app()

if __name__ == "__main__":
    main()
