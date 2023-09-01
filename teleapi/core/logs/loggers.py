import inspect
import logging
import os
import sys
from functools import wraps
from typing import Any

from .formats import FileLogFormatter, ConsoleLogFormatter
from datetime import datetime

file_log_formatter = FileLogFormatter()
console_log_formatter = ConsoleLogFormatter()


def setup_logger(name: str, logs_dir: str = None, console_log_level: int = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logs_dir is not None:
        os.makedirs(logs_dir,  exist_ok=True)

        info_file_handler = logging.FileHandler(filename=os.path.join(logs_dir, 'info.log'), encoding='utf-8')
        info_file_handler.setFormatter(file_log_formatter)
        info_file_handler.setLevel(logging.INFO)

        debug_file_handler = logging.FileHandler(filename=os.path.join(logs_dir, 'debug.log'), encoding='utf-8')
        debug_file_handler.setFormatter(file_log_formatter)
        debug_file_handler.setLevel(logging.DEBUG)

        logger.addHandler(info_file_handler)
        logger.addHandler(debug_file_handler)

    if console_log_level is not None:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(console_log_formatter)
        console_handler.setLevel(console_log_level)
        logger.addHandler(console_handler)

    return logger


def log_async_methods(logger_name: str = None, log_result: bool = False, log_level: int = logging.DEBUG):
    def decorator(cls):
        def get_wrapper(func):
            logger = logging.getLogger(logger_name if logger_name is not None else f"teleapi_calls.{cls.__module__}.{cls.__name__}")

            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                logger.log(log_level, f"Called method {func.__name__} of class {cls.__name__}")

                result = await func(*args, **kwargs)

                if log_result:
                    logger.log(log_level, f"Got result form method {func.__name__} of class {cls.__name__}: {result}")

                return result

            return wrapper

        for attr in dir(cls):
            if attr.startswith("__"):
                continue

            value = getattr(cls, attr)

            if inspect.iscoroutinefunction(value):
                setattr(cls, attr, get_wrapper(value))

        return cls

    return decorator


def setup_teleapi_logger(logs_dir: str = None, create_files: bool = False, console_log_level: int = logging.INFO):
    logs_dir = os.path.join('logs', 'teleapi', datetime.now().strftime('%Y-%m-%d %H-%M-%S')) if logs_dir is None else logs_dir
    return setup_logger(
        name="teleapi",
        logs_dir=logs_dir if create_files else None,
        console_log_level=console_log_level
    )
