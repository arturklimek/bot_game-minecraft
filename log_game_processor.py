import re
import threading
import time
from typing import Callable
from app_config import get_game_latest_log_path, get_risk_nicks_list
from logger import app_logger

def log_new_line(line: str) -> None:
    app_logger.debug(f"New line in game latest log file: {line.strip()}")

def watcher(file_path: str = get_game_latest_log_path(), action: Callable[[str], None] = log_new_line) -> None:
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
                    time.sleep(20)
                    continue
                action(line)
    except FileNotFoundError:
        app_logger.error(f"The file at {file_path} was not found.")
    except IOError as e:
        app_logger.error(f"An I/O error occurred: {e}")
    except Exception as e:
        app_logger.error(f"An unexpected error occurred: {e}")

def start_watcher_thread(action: Callable[[str], None] = log_new_line) -> None:
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
        return None

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
