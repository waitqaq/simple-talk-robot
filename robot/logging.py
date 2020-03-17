from logging import FileHandler
from robot import constants
import logging


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
def getLogger(name):
    # 打印log，名字为函数名，级别为DEBUG，
    logger = logging.getLogger(name)
    logger.setLevel(INFO)
    file_handler = FileHandler(constants.LOGGING_PATH)
    logger.addHandler(file_handler)
    return logger