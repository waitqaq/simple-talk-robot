from logging import FileHandler
from robot import constants
import logging
import subprocess


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

def readLog(lines=200):
    """
    获取最新的指定行数

    :param lines: 最大行数
    :return: 最新指定行数的log
    """
    res =subprocess.run(['tail','-n', str(lines), constants.LOGGING_PATH],
                        cwd=constants.APP_PATH,stdout=subprocess.PIPE, encoding='utf-8')
    return res.stdout

def read_active_log():
    res =subprocess.run(['tail','-n',str(1000), constants.ACTIVE_LOGGING_PATH],
                        cwd=constants.APP_PATH,stdout=subprocess.PIPE, encoding='utf-8')
    return res.stdout


