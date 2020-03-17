from robot import config, logging
from .sdk import XunfeiSpeech, BaiduSpeech


logger = logging.getLogger(__name__)

class AbstractTTS(object):

    def get_speech(self, phrase):
        pass


class XunfeiTTS(AbstractTTS):
    SLUG = "xunfei-tts"

    def __init__(self):
        items = config.get('/xunfei_yuyin')
        self.appid = items['appid']
        self.apikey = items['apikey']
        self.apiSecret = items['apiSecret']
        self.voice_name = items['voice_name']
        # 音频编码(raw合成的音频格式pcm、wav,lame合成的音频格式MP3)
        self.aue = 'lame'

    def get_speech(self, phrase):
        return XunfeiSpeech.synthesize(phrase, self.appid, self.apikey, self.apiSecret, self.voice_name)


class BaiduTTS(AbstractTTS):
    SLUG = "baidu-tts"

    def __init__(self):
        items = config.get('/baidu_yuyin')
        self.apikey = items['apikey']
        self.apiSecret = items['apiSecret']
        self.voice_name = items['voice_name']

    def get_speech(self, phrase):
        return BaiduSpeech.synthesize(phrase, self.apikey, self.apiSecret, self.voice_name)


def get_engine_by_slug(slug=None):

    if not slug or type(slug) is not str:
        raise TypeError("无效的 TTS slug '%s'", slug)
    #
    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                              engine.SLUG == slug, get_engines()))
    if len(selected_engines) == 0:
        raise ValueError("错误：找不到名为 {} 的 TTS 引擎".format(slug))
    else:
        if len(selected_engines) > 1:
            logger.warning("注意: 有多个 TTS 名称与指定的引擎名 {} 匹配").format(slug)
        engine = selected_engines[0]
        logger.info("使用 {} TTS 引擎".format(engine.SLUG))
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
            list(get_subclasses(AbstractTTS))
            if hasattr(engine, 'SLUG') and engine.SLUG]
