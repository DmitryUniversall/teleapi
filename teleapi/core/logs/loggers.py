import logging
import os
from .formats import FileLogFormatter, ConsoleLogFormatter
from datetime import datetime

file_log_formatter = FileLogFormatter()
console_log_formatter = ConsoleLogFormatter()


def setup_logger(name: str, logs_dir: str = None, console_log_level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logs_dir is not None:
        os.mkdir(logs_dir)

        info_file_handler = logging.FileHandler(filename=os.path.join(logs_dir, 'info.log'), encoding='utf-8', mode='w')
        info_file_handler.setFormatter(file_log_formatter)
        info_file_handler.setLevel(logging.INFO)

        debug_file_handler = logging.FileHandler(filename=os.path.join(logs_dir, 'debug.log'), encoding='utf-8', mode='w')
        debug_file_handler.setFormatter(file_log_formatter)
        debug_file_handler.setLevel(logging.DEBUG)

        logger.addHandler(info_file_handler)
        logger.addHandler(debug_file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_log_formatter)
    console_handler.setLevel(console_log_level)

    logger.addHandler(console_handler)

    return logger


def setup_teleapi_logger(logs_dir: str = None, create_files: bool = False, console_log_level: int = logging.INFO):
    logs_dir = os.path.join('logs', 'teleapi', datetime.now().strftime('%Y-%m-%d %H-%M-%S')) if logs_dir is None else logs_dir
    return setup_logger(
        name="teleapi",
        logs_dir=logs_dir if create_files else None,
        console_log_level=console_log_level
    )
