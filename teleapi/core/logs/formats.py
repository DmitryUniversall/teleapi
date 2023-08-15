import logging


class LogFormatter(logging.Formatter):
    format_ = """[%(asctime)s]\npath = %(pathname)s\nlevel = %(levelname)s\nlogger = %(name)s\nplace = %(filename)s; in '%(funcName)s'; line %(lineno)d\nmessage = %(message)s\n"""

    def format(self, record):
        log_fmt = self.format_
        formatter = logging.Formatter(fmt=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


class LogFormatterColor(LogFormatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.FORMATS = {
            logging.DEBUG: self.grey + self.format_ + self.reset,
            logging.INFO: self.grey + self.format_ + self.reset,
            logging.WARNING: self.yellow + self.format_ + self.reset,
            logging.ERROR: self.red + self.format_ + self.reset,
            logging.CRITICAL: self.bold_red + self.format_ + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(fmt=log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


class ConsoleLogFormatter(LogFormatterColor):
    format_ = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"


class FileLogFormatter(LogFormatter):
    format_ = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s; in '%(funcName)s':%(lineno)d)"
