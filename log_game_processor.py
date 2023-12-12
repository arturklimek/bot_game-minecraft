import re
import threading
import time
from typing import Callable
from app_config import game_latest_log_path
from logger import app_logger

def log_new_line(line: str) -> None:
    app_logger.debug(f"New line in game latest log file: {line.strip()}")

def watcher(file_path: str = game_latest_log_path, action: Callable[[str], None] = log_new_line) -> None:
    """
    Monitors a log file for new entries and performs an action on each new line.

    Args:
        file_path (str): Path to the log file to be monitored. Defaults to game_latest_log_path.
        action (Callable[[str], None]): A function to be called with each new line as its argument.
    """
    with open(file_path, 'r') as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            action(line)

def start_watcher_thread(file_path: str = game_latest_log_path, action: Callable[[str], None] = log_new_line) -> None:
    """
    Starts the watcher function in a separate thread.

    Args:
        file_path (str): Path to the log file to be monitored. Defaults to game_latest_log_path.
        action (Callable[[str], None]): A function to be called with each new line as its argument.
    """
    watcher_thread = threading.Thread(target=watcher, args=(file_path, action))
    watcher_thread.daemon = True
    watcher_thread.start()

def is_chat_player_message(log_line: str) -> bool:
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
            app_logger.debug("The readed line form game logs is Chat Player Message")
            return True
        else:
            app_logger.debug("The readed line form game logs is NOT Chat Player Message")
            return False
    else:
        app_logger.debug("The readed line form game logs contain unknown content")
        return None

def extract_player_name(log_line: str) -> str:
    """
    Extracts the player's name from a chat message.

    Args:
        log_line (str): The line from the log file containing the chat message.

    Returns:
        str: The extracted player name.
    """
    if is_chat_player_message(log_line):
        try:
            parts = log_line.split("]: ")
            if len(parts) > 1:
                chat_part = parts[1]
                if "[CHAT]" in chat_part:
                    chat_sections = chat_part.split(" [")
                    if len(chat_sections) > 2:
                        name_section = chat_sections[-3]
                        player_name = name_section.split(" ")[-1]
                        return player_name
        except Exception as ex:
            app_logger.error(f"Error extracting player name: {ex}")
    return ""

def extract_player_message(log_line: str) -> str:
    """
    Extracts the player's chat message from a chat log line.

    Args:
        log_line (str): The line from the log file containing the chat message.

    Returns:
        str: The extracted chat message.
    """
    if is_chat_player_message(log_line):
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
                    return message[1]
        except Exception as ex:
            app_logger.error(f"Error extracting player name: {ex}")
    return ""
