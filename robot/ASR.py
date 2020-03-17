from robot import config
from .sdk import XunfeiSpeech,BaiduSpeech
from robot import logging


logger = logging.getLogger(__name__)

class AbstractASR(object):

    def transcribe(self, fpath):
        pass


class XunfeiASR(AbstractASR):
    """
    讯飞语音识别
    """
    SLUG = "xunfei-asr"

    def __init__(self):
        items = config.get('/xunfei_yuyin')
        self.appid = items['appid']
        self.apikey = items['apikey']
        self.apiSecret = items['apiSecret']


    def transcribe(self, fp):
        return XunfeiSpeech.transcribe(fp, self.appid, self.apikey, self.apiSecret)


class BaiduASR(AbstractASR):
    """
    百度语音识别
    """
    SLUG = "baidu-asr"

    def __init__(self):
        items = config.get('/baidu_yuyin')
        self.apikey = items['apikey']
        self.apiSecret = items['apiSecret']


    def transcribe(self, fp):
        return BaiduSpeech.transcribe(fp, self.apikey, self.apiSecret)


def get_engine_by_slug(slug=None):

    if not slug or type(slug) is not str:
        raise TypeError("无效的 ASR slug '%s'", slug)
    #
    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("错误：找不到名为 {} 的 ASR 引擎".format(slug))
    else:
        if len(selected_engines) > 1:
            logger.warning("注意: 有多个 ASR 名称与指定的引擎名 {} 匹配").format(slug)
        engine = selected_engines[0]
        logger.info("使用 {} ASR 引擎".format(engine.SLUG))
        return engine.SLUG

def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    # 如果engine等于"SLUG"并且SLUG存在内容，则返回engine
    return [engine for engine in
            list(get_subclasses(AbstractASR))
            if hasattr(engine, 'SLUG') and engine.SLUG]