import yaml
from robot import constants, logging
import os

_config = {}
# 　一个标记ｂｏｏｌ值
has_init = True
logger = logging.getLogger(__name__)

def init():
    global _config, has_init
    # 读取配置文件的配置
    with open(constants.CONFIG_PATH, 'r') as f:
        _config = yaml.safe_load(f)
        has_init = True

def get_path(items, default):
    global _config
    curConfig = _config
    # 如果items为字符串，并且第一个为'/'
    if isinstance(items, str) and items[0] == '/':
        # 按第一个/ 进行拆分为数组
        items = items.split('/')[1:]
    for key in items:
        # 如果在配置文件中找到了，那么就将vuale值拿出来
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            logger.warning('没有找到配置{}，使用默认值{}'.format('/'.join(items), default))
            return default
    # 返回value值
    return curConfig

def has_path(items):
    global _config
    curConfig = _config
    # 如果items为字符串，并且第一个为'/'
    if isinstance(items, str) and items[0] == '/':
        # 按第一个/ 进行拆分为数组
        items = items.split('/')[1:]
    for key in items:
        # 如果在配置文件中找到了，那么就将vuale值拿出来
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            return False
    return True

def get(item, default=None):
    """
    获取配置文件的值

    :param item : 配置项名，如果是多级配置，则以 '/a/b' 或者  ['a', 'b']的形式
    :param default:  默认值（可选）
    :returns: 如果没有该配置，则提供一个默认值
    """
    global has_init, _config
    # 如果读取到了，执行
    if has_init:
        init()
    #　如果没有数据，直接返回配置文件内容
    if not item:
        return _config
    return get_path(item, default)

def has(item):
    """
    判断是否有某个配置

    :param item : 配置项名，如果是多级配置，则以 '/a/b' 或者  ['a', 'b']的形式
    :returns: 是否有这个配置
    """
    global has_init, _config
    # 如果读取到了，执行
    if has_init:
        init()
    return has_path(item)

def getText():
    """
    获取配置文件的文本内容

    :returns :配置文件中的内容
    """
    if os.path.exists(constants.getConfigPath()):
        with open(constants.getConfigPath(), 'r') as f:
            return f.read()
    logger.error('配置文件不存在')
    return ''

def dump(configStr):
    """
    将配置字符串写回配置文件

    :param configStr: 配置字符串
    """
    with open(constants.getConfigPath(), 'w') as f:
        f.write(configStr)