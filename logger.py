import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
import sys

def setup_logger() -> Logger:
    """
    Sets up and configures the logger for the application.

    This function creates a logger named 'app_logger'. It sets up a file handler for logging into a file named 'app.log' with a rotating file handler, keeping backups of the last two log files, each up to 5MB.
    It also sets up a console handler for logging output to stdout. Both handlers have their own formatting for log messages.

    Returns:
        A configured logger object.
    """
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('app.log', maxBytes=5000000, backupCount=2, encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - (%(filename)s:%(lineno)d) - %(message)s')
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

app_logger = setup_logger()
