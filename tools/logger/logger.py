import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
