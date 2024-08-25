import logging

class LoggingFormatter(logging.Formatter):
    green  = "\x1b[32;20m"
    cyan   = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red    = "\x1b[31;20m"
    reset  = "\x1b[0m"
    format = "[%(asctime)s] %(filename)-15s l.%(lineno)-5s - %(levelname)-7s -> %(message)s"

    FORMATS = {
        logging.DEBUG:   green  + format + reset,
        logging.INFO:    cyan   + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR:   red    + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        formatter.datefmt = "%H:%M:%S"
        return formatter.format(record)

def setLogger():
    logger = logging.getLogger("Sudoku Logger")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(LoggingFormatter())
    logger.addHandler(ch)
    return logger

global logger
logger = setLogger()
