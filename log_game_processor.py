import sys
import threading
import time
from datetime import datetime, timedelta
from typing import Callable
from activities.afk import afk_on_spawn
from activities.chat import send_private_message_to_player, send_chat_message_to_player, send_on_chat
from app_config import get_game_latest_log_path, get_risk_nicks_list, get_messages_respond_dict, \
    get_chat_message_answer_flag, get_private_message_answer_flag, get_client_player_nickname, \
    get_counter_risk_messages_to_lobby, get_counter_risk_messages_to_afk
from logger import app_logger

reply_data = {}

def get_reply_data() -> dict:
    return reply_data

life_time_risk_messages = 5
counter_risk_messages = 0

def get_counter_risk_messages() -> int:
    return counter_risk_messages

timestamp_last_riks_message = None

def set_reply_data(new_reply_data: dict) -> None:
    global reply_data
    app_logger.debug(f"change sender_player_data: {reply_data} to nev value: {new_reply_data}")
    reply_data = new_reply_data

def clear_reply_data() -> None:
    global reply_data
    reply_data = {}

def update_reply_data(log_line: str) -> None:
    """
    Updates reply data based on the content of a log line from the game.

    This function processes a log line to extract a player's nickname and the content of their message.
    If the nickname is identified as risky, it prepares a reply using a predefined response dictionary.
    The extracted and processed information is then stored in a global `reply_data` dictionary.

    Args:
        log_line (str): The log line from the game to be analyzed.

    Global Variables:
        reply_data (dict): A global dictionary updated with the nickname of the player and the corresponding reply.
    """
    global counter_risk_messages
    global reply_data
    global timestamp_last_riks_message
    private_message_status = False
    player_nickname = ""
    message_content = ""
    if get_chat_message_answer_flag():
        if is_player_chat_message(log_line):
            content = extract_content_from_player_chat_message(log_line).lower().strip()
            client_nickname = get_client_player_nickname().lower().strip()
            if client_nickname in content:
                player_nickname = extract_nick_from_player_chat_message(log_line).lower().strip()
                message_content = content.replace(client_nickname, '')
                message_content.strip()
                private_message_status = False
    if get_private_message_answer_flag():
        if is_player_private_message(log_line):
            player_nickname = extract_nick_from_player_private_message(log_line).lower().strip()
            message_content = extract_content_from_player_private_message(log_line).lower().strip()
            private_message_status = True
    if player_nickname and message_content:
        if check_risk_nickname(player_nickname):
            # app_logger.info("Find chat msessage sended from nick: {player_nickname}")
            messages_respond_dict = get_messages_respond_dict()
            answer = "?"
            if message_content in messages_respond_dict.keys():
                answer = messages_respond_dict[message_content]
                app_logger.debug(f"message_content is in messages_respond_dict, change answer value: {answer}")
            if timestamp_last_riks_message:
                time_difference = datetime.now() - timestamp_last_riks_message
                if time_difference <= timedelta(minutes=life_time_risk_messages):
                    counter_risk_messages = counter_risk_messages + 1
                else:
                    counter_risk_messages = 0
            reply_data = {
                "private": private_message_status,
                "nickname": player_nickname,
                "answer": answer,
            }
            timestamp_last_riks_message = datetime.now()
            app_logger.info(
                f"detected message from player_nickname: {player_nickname} in risk_nicks_list, set sender_player_data value to: {reply_data}")
    else:
        app_logger.debug(f"Needed variable is empty, player_nickname: {player_nickname} message_content: {message_content}")

def make_reply() -> bool: # TODO: dodać zależność odpowiedzi na podstawie konfiguracji - odpowiednich flag // lub w update_reply_data + licznik ...
    """
    Sends a reply message based on the data stored in the 'reply_data' dictionary.

    This function checks if 'reply_data' contains valid data and sends either a private or a public chat message to the player depending on the 'private' flag in the dictionary. After sending the message, it clears the 'reply_data' dictionary.

    Returns:
        bool: True if a reply was sent, False if 'reply_data' is empty.
    """
    global reply_data
    if reply_data:
        if reply_data["private"]:
            send_private_message_to_player(nickname=reply_data["nickname"], reply_text=reply_data["answer"])
        else:
            send_chat_message_to_player(nickname=reply_data["nickname"], reply_text=reply_data["answer"])
        reply_data.clear()
        app_logger.debug(f"make_reply send reply - reply_data: {reply_data}")
        return True
    else:
        app_logger.debug("Return False - reply_data is empty")
        return False

def make_risk_afk() -> None:
    """
    Initiates an AFK action based on the number of risk messages received.

    This function checks if the number of risk messages ('counter_risk_messages') has reached a threshold specified in 'get_counter_risk_messages_to_afk'. If the threshold is met, it triggers an AFK action at the spawn location for a duration calculated based on certain criteria.
    """
    global counter_risk_messages
    if get_counter_risk_messages_to_afk() > 0:
        if counter_risk_messages >= get_counter_risk_messages_to_afk():
            afk_time = 0
            afk_on_spawn(afk_time)

def make_risk_exit() -> None:
    """
    Exits the program if the number of risk messages reaches a certain threshold.

    This function checks if the count of risk messages ('counter_risk_messages') has reached a set limit, specified in 'get_counter_risk_messages_to_lobby'. If the limit is reached, it sends a command to move the player to the lobby and then exits the program.

    Note:
        The exit command currently stops the entire program. It is recommended to change this behavior to only disable certain tasks or functions instead of exiting the entire application.
    """
    if get_counter_risk_messages_to_lobby() > 0:
        if counter_risk_messages >= get_counter_risk_messages_to_lobby():
            lobby_command = "/lobby 1"
            time.sleep(1)
            app_logger.info(f"Go to Lobby - execute command: {lobby_command}")
            send_on_chat(lobby_command)
            time.sleep(5)
            app_logger.info("Exit Program")
            sys.exit() #TODO: change exit to disable working tasks - not all program

def check_risk_nickname(nickname: str) -> bool:
    """
    Checks if a given nickname is in the list of risk nicknames.

    This function compares the provided nickname, after converting it to lowercase and stripping any whitespace, against a list of predefined 'risk' nicknames. The list of risk nicknames is obtained from the 'get_risk_nicks_list' function and is also processed to be in lowercase and stripped of whitespace.

    Args:
        nickname (str): The player's nickname to be checked.

    Returns:
        bool: True if the nickname is found in the risk nicknames list, False otherwise.
    """
    risk_nicks_list = list(map(lambda x: x.lower().strip(), get_risk_nicks_list()))
    if nickname.lower().strip() in risk_nicks_list:
        app_logger.debug(f"Nick: {nickname} IS in risk_nicks_list")
        return True
    else:
        app_logger.debug(f"Nick: {nickname} IS NOT in risk_nicks_list")
        return False

def watcher(file_path: str = get_game_latest_log_path(), action: Callable[[str], None] = update_reply_data) -> None:
    """
    Monitors a log file for new entries and performs an action on each new line.

    Args:
        file_path (str): Path to the log file to be monitored. Defaults to game_latest_log_path.
        action (Callable[[str], None]): A function to be called with each new line as its argument.
    """
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            file.seek(0, 2)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                app_logger.debug(f"Readed line: {line}")
                action(line)
    except FileNotFoundError:
        app_logger.error(f"The file at {file_path} was not found.")
    except IOError as e:
        app_logger.error(f"An I/O error occurred: {e}")
    except Exception as e:
        app_logger.error(f"An unexpected error occurred: {e}")

def start_messages_watcher_thread(action: Callable[[str], None] = update_reply_data) -> None:
    """
    Starts the watcher function in a separate thread.

    Args:
        file_path (str): Path to the log file to be monitored. Defaults to game_latest_log_path.
        action (Callable[[str], None]): A function to be called with each new line as its argument.
    """
    file_path = get_game_latest_log_path()
    watcher_thread = threading.Thread(target=watcher, args=(file_path, action))
    watcher_thread.daemon = True
    watcher_thread.start()

def is_player_chat_message(log_line: str) -> bool:
    """
    Determines if a given log line is a player chat message.

    This function analyzes a line from a game log to determine whether it represents a chat message sent by a player.
    It checks for specific indicators that are characteristic of player messages in the chat. The function looks for
    the presence of the '[CHAT]' indicator and then verifies if the message is from the global ('[G]') or party ('[P]')
    chat, which are typical identifiers of player messages.

    Args:
        log_line (str): The log line to be analyzed.

    Returns:
        bool: True if the line is a player chat message, False if it is not a player message, or if the '[CHAT]'
              indicator is not present.
    """
    chat_indicators = "[CHAT]"
    player_message_indicators = ["[G]", "[P]"]
    if chat_indicators in log_line:
        if player_message_indicators[0] in log_line or player_message_indicators[1] in log_line:
            app_logger.debug("The readed line form game logs is Player Chat Message")
            return True
        else:
            app_logger.debug("The readed line form game logs is NOT Player Chat Message")
            return False
    else:
        app_logger.debug("The readed line form game logs contain unknown content")

def is_player_private_message(log_line: str) -> bool:
    """
    Determines if a given log line is a private chat message received in the game.

    Args:
        log_line (str): The log line to be analyzed.

    Returns:
        bool: True if it's a private chat message, False otherwise.

    This function checks for specific patterns in the log line that indicate a private chat message.
    It looks for '[CHAT]' followed by a structure '[... -> ja]' which signifies a private message received by the player.
    """
    chat_indicator = "[CHAT]"
    private_message_indicator = "-> ja]"
    if chat_indicator in log_line and private_message_indicator in log_line:
        app_logger.debug("The readed line from game logs is a Player Private Message")
        return True
    else:
        app_logger.debug("The readed line from game logs is NOT a Player Private Message")
        return False

def extract_nick_from_player_chat_message(log_line: str) -> str:
    """
    Extracts the player's name from a chat message.

    Args:
        log_line (str): The line from the log file containing the chat message.

    Returns:
        str: The extracted player name.
    """
    if is_player_chat_message(log_line):
        try:
            parts = log_line.split("]: ")
            if len(parts) > 1:
                chat_part = parts[1]
                if "[CHAT]" in chat_part:
                    chat_sections = chat_part.split(" [")
                    if len(chat_sections) > 2:
                        name_section = chat_sections[-3]
                        player_name = name_section.split(" ")[-1]
                        app_logger.debug(f"player_name: {player_name}")
                        return player_name
            app_logger.debug(f"Can not extrack nick from log_line: {log_line}")
        except Exception as ex:
            app_logger.error(f"Error extracting player name: {ex}")
    return ""


def extract_nick_from_player_private_message(log_line: str) -> str:
    """
    Extracts the sender's nickname from a private chat message.

    Args:
        log_line (str): The log line containing the private chat message.

    Returns:
        str: The nickname of the sender of the private message.

    This function looks for the pattern indicating a private message and extracts the sender's nickname
    which precedes the '-> ja]' pattern.
    """
    if is_player_private_message(log_line):
        start_idx = log_line.find("[CHAT]") + len("[CHAT]")
        end_idx = log_line.find("-> ja]")
        if start_idx != -1 and end_idx != -1:
            sender_segment = log_line[start_idx:end_idx]
            sender_nickname = sender_segment.split()[-1]
            app_logger.debug(f"sender_nickname: {sender_nickname.strip()}")
            return sender_nickname.strip()
        else:
            app_logger.debug(f"Can not extract player nickname form log_line: {log_line}")
            return ""

def extract_content_from_player_chat_message(log_line: str) -> str:
    """
    Extracts the player's chat message from a chat log line.

    Args:
        log_line (str): The line from the log file containing the chat message.

    Returns:
        str: The extracted chat message.
    """
    if is_player_chat_message(log_line):
        try:
            parts = log_line.split(" [")
            last_part = ""
            for part in parts[::-1]:
                if "]" in part and ":" in part:
                    last_part = part
                    break
            if last_part:
                message = last_part.split("]: ", 1)
                if len(message) > 1:
                    app_logger.debug(f"message: {message[1]}")
                    return message[1]
            else:
                app_logger.debug(f"Can not extract content from log_line: {log_line}")
        except Exception as ex:
            app_logger.error(f"Error extracting player name: {ex}")
    return ""

def extract_content_from_player_private_message(log_line: str) -> str:
    """
    Extracts the content of a private chat message.

    Args:
        log_line (str): The log line containing the private chat message.

    Returns:
        str: The content of the private chat message.

    This function looks for the pattern indicating a private message and extracts the content
    that follows the '-> ja]' pattern.
    """
    if is_player_private_message(log_line):
        start_idx = log_line.find("-> ja]") + len("-> ja]")
        if start_idx != -1:
            message_content = log_line[start_idx:].strip()
            app_logger.debug(f"message_content: {message_content}")
            return message_content
        else:
            app_logger.debug(f"Can not extract content form log_line: {log_line}")
            return ""
