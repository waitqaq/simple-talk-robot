import pkgutil
from robot.sdk.AbstractPlugin import AbstractPlugin
from robot import config, logging


logger = logging.getLogger(__name__)
class Brain(object):

    def __init__(self, con):
        # 回话模块
        self.con = con
        self.plugins = self.init_plugins()

    def hasDisbale(self, name):
        if config.has('/{}/enable'.format(name)):
            if not config.get('/{}/enable'.format(name)):
                logger.info('插件{}已被禁用'.format(name))
                return True
        return False

    def init_plugins(self):
        """
        读取所有插件
        """
        #  产生一个包含本地文件名为plugins下的所有模块的迭代器,通过遍历取值
        plugins = []
        for finder, name, ispkg in pkgutil.walk_packages(['plugins']):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except Exception as e:
                logger.error(e)
                continue
            # 判断是否包含名为Plugin的类，并判断该类是不是AbstrPlugin的基类
            if hasattr(mod, 'Plugin') and issubclass(mod.Plugin, AbstractPlugin) and not self.hasDisbale(name):
                plugins.append(mod.Plugin(self.con))
        return plugins

    # 相应用户的值
    def doQuery(self, query):

        for plugin in self.plugins:
            # 命中技能
            if plugin.isValid(query):

                plugin.handle(query)
                return True
        return False
