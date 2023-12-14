import time
from datetime import datetime, timedelta
import keyboard
from app_config import get_command_sethome, get_command_home_tmp, get_command_spawn, \
    get_command_home_repair, get_command_home_mining, get_command_home_chest, get_command_home_farm, \
    get_command_sell_inventory, get_hotkey_enter, get_hotkey_chat, get_chat_messages_flag, \
    get_chat_messages_frequency_min, get_chat_messages
from delay import return_random_wait_interval_time
from logger import app_logger

last_message_time = datetime.now()
chat_message_id = 0

def send_chat_notification() -> None:
    """
    Sends a chat notification based on the configured messages and frequency.

    This function checks if the conditions for sending a chat message are met, including the frequency and flag for chat messages, and sends a message accordingly.
    """
    global last_message_time
    global chat_message_id
    app_logger.debug("send_chat_notification was used")
    try:
        current_time = datetime.now()
        chat_messages_len = len(get_chat_messages())
        if get_chat_messages_flag() and current_time - last_message_time >= timedelta(minutes=get_chat_messages_frequency_min()) and chat_messages_len > 0:
            time.sleep(return_random_wait_interval_time(0.25, 1))
            send_on_chat(get_chat_messages()[chat_message_id])
            chat_message_id = chat_message_id + 1
            if chat_message_id >= chat_messages_len:
                chat_message_id = 0
            time.sleep(return_random_wait_interval_time(0.25, 1))
            last_message_time = current_time
        else:
            app_logger.debug(f"The conditions were not met chat_messages_flag: {get_chat_messages_flag()} chat_messages_len {chat_messages_len} last_message_time: {last_message_time}")
    except Exception as ex:
        app_logger.error(ex)

def send_on_chat(text: str) -> None:
    """
    Sends a specified text message in the game chat.

    Args:
        text: The text message to be sent in the chat.

    The function simulates keyboard inputs to open the chat, type the message, and send it.
    """
    app_logger.debug("send_on_chat was used")
    # keyboard.press_and_release(get_hotkey_esc())
    # time.sleep(return_random_wait_interval_time())
    # keyboard.press_and_release(get_hotkey_esc())
    # time.sleep(return_random_wait_interval_time())
    keyboard.press_and_release(get_hotkey_chat())
    app_logger.debug(f"Press and release {get_hotkey_chat()}")
    time.sleep(return_random_wait_interval_time(0.75,1.5))
    keyboard.write(text)
    app_logger.debug(f"write: {text}")
    time.sleep(return_random_wait_interval_time(0.75,1.5))
    keyboard.press_and_release(get_hotkey_enter())
    app_logger.debug(f"Press and release {get_hotkey_enter()}")

def send_chat_message_to_player(nickname: str = "", reply_text: str = "") -> None:
    message_text = ""
    if nickname:
        message_text = nickname + " "
        app_logger.debug("nickname is empty")
    if reply_text:
        message_text = message_text + reply_text
        send_on_chat(message_text)
    else:
        app_logger.debug("can not send player chat message - reply_text is empty")

def send_private_message_to_player(nickname: str = "", reply_text: str = "") -> None:
    if nickname and reply_text:
        message_text = f"/msg {nickname} {reply_text}"
        send_on_chat(message_text)
    else:
        app_logger.debug("can not send player private message - reply_text or reply_text is empty")

def tp_to_repair_home() -> None:
    """
    Teleports the player to a predefined 'repair' home location in the game.

    This function sends a teleport command to the game chat to move the player to the 'repair' home.
    """
    app_logger.debug("tp_to_repair_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_home_repair())

def tp_to_mining_home() -> None:
    """
    Teleports the player to a predefined 'mining' home location in the game.

    This function sends a teleport command to the game chat to move the player to the 'mining' home.
    """
    app_logger.debug("tp_to_mining_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_home_mining())

def tp_to_chest_home() -> None:
    """
    Teleports the player to a predefined 'chest' home location in the game.

    This function sends a teleport command to the game chat to move the player to the 'chest' home.
    """
    app_logger.debug("tp_to_chest_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_home_chest())

def tp_to_farm_home(index: int) -> None:
    """
    Teleports the player to a predefined 'farm' home location in the game, specified by an index.

    Args:
        index: The index of the farm home to which the player will be teleported.

    This function sends a teleport command to the game chat to move the player to the specified 'farm' home.
    """
    app_logger.debug("tp_to_farm_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(f"{get_command_home_farm()}{index}")

def tp_to_tmp_home() -> None:
    """
    Teleports the player to a temporary home location in the game.

    This function sends a teleport command to the game chat to move the player to a temporary home.
    """
    app_logger.debug("tp_to_tmp_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_home_tmp())

def tp_to_spawn() -> None:
    """
    Teleports the player to the spawn location in the game.

    This function sends a teleport command to the game chat to move the player to the game's spawn location.
    """
    app_logger.debug("tp_to_spawn was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_spawn())

def set_tmp_home() -> None:
    """
    Sets the current location as the temporary home in the game.

    This function sends a command to the game chat to set the player's current location as a temporary home.
    """
    app_logger.debug("set_tmp_home was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_sethome() + " " + get_command_home_tmp()[6:])

def sellall_inventory() -> None:
    """
    Executes the command to sell all items in the player's inventory in the game.

    This function sends a command to the game chat to initiate the selling of all items in the player's inventory.
    """
    app_logger.debug("sellall_inventory was used")
    time.sleep(return_random_wait_interval_time())
    send_on_chat(get_command_sell_inventory())
