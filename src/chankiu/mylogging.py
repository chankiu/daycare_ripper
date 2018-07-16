import logging
from logging.handlers import RotatingFileHandler

def log(app_name):
    # create logger with 'app_name'
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = RotatingFileHandler(filename='app_name.log', maxBytes=2048, backupCount=3)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger