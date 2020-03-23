import os

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir))
CONFIG_PATH = 'config.yml'
LOGGING_PATH = 'wukong.log'
ACTIVE_LOGGING_PATH = 'actives.log'
def getConfigPath():
    """
    返回配置文件的完整路径
    """
    return os.path.join(APP_PATH, CONFIG_PATH)