import threading
import keyboard
import os
from activities.chat import sellall_inventory
from activities.chest import update_chest_patterns_sizes
from activities.equipment import update_eq_patterns_sizes
from activities.farm import toggle_farm_procedure
from activities.mine import toggle_mine_procedure
from app_config import OUTPUTS_DIR_PATH, PATTERNS_DIR_PATH, setup_config_file, get_button_mine_procedure, \
    get_button_farm_procedure
from clicker import setup_autoclicer_hotkeys
from logger import app_logger
from patterns import load_patterns_all
from screenshooter import start_screenshot_thread

lock = threading.Lock()

def prepare_folders():
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

def sellall_inventory_thread():
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
    # keyboard.add_hotkey(82, test) # test key 'insert' on numpad
    setup_autoclicer_hotkeys()
    # keyboard.wait('esc')
    app_logger.debug(f"Setup buttons are done")


def main():
    """
    Main function to initiate the application.
    Performs initial setup including loading configuration, preparing folders, loading patterns, updating sizes, setting up buttons, and starting the screenshot thread.
    Waits for a specific keypress ('-' on numpad) to stop the application.
    Logs the start and stop of the application.

    TODO: dodać zabezpieczenia aby aplikacja wykonywała czynności tylko gdy okno gry jest aktywne (ma focus)
    TODO: dodanie procedury która sprawi, że okno będzie aktywne oraz zmieni cztery razy tryb okna gry klikajac f11 -  problem występuje przy trybie pełnoekranowym oraz alt+tab
    """
    setup_config_file()
    prepare_folders()
    load_patterns_all()
    update_eq_patterns_sizes()
    update_chest_patterns_sizes()
    setup_buttons()
    start_screenshot_thread()

    print("Application started.")
    app_logger.info(f"Application started")
    print("Press '+' on numpad to start mine procedure.")
    print("Press '-' on numpad to stop app.")

    keyboard.wait(74)  # test key '-' on numpad
    app_logger.info(f"User stop app.")

if __name__ == "__main__":
    main()
