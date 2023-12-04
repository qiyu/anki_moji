import logging
import sys

moji_server = None

_logger_initialized = False


def get_logger() -> logging.Logger:
    global _logger_initialized

    logger = logging.getLogger("anki_moji")
    if not _logger_initialized:
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        _logger_initialized = True
    return logger
