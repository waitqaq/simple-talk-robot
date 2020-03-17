from robot import Player, ASR, TTS, AI, utils
from robot.Brain import Brain
from robot import logging, config
from robot import ASR
from robot import TTS

logger = logging.getLogger(__name__)


class Conversation():

    # 创建一个对话方法
    def converse(self, fp):
        # 播放唤醒后提示音
        global asr,asr_slug
        Player.player('static/beep_lo.wav', False)
        asr_slug = ASR.get_engine_by_slug(config.get('/asr_engine'))
        self.do_ASR(asr_slug)
        # 将语音翻译为文本
        query = asr.transcribe(fp)
        logger.info(query)
        # 删除临时存在的语音文件
        utils.check_and_delete(fp)
        brain = Brain(self)
        if not brain.doQuery(query):

            ai = AI.TulingRobot()
            # 进行回答，并返回回答文本
            phrase = ai.chat(query)
            logger.info(phrase)
            self.say(phrase, True)


    def say(self, phrase, delete=False):
        """
        播放
        """
        # 实例化播放的方法
        global tts
        player = Player.SoxPlayer()
        # 实例化语音合成的方法
        tts_slug = TTS.get_engine_by_slug(config.get('/tts_engine'))
        self.do_TTS(tts_slug)
        # 得到需要播放的音频进行播放
        fp = tts.get_speech(phrase)
        player.play(fp, True)

    def do_ASR(self, asr_slug):
        global asr
        if asr_slug == 'xunfei-asr':
            asr = ASR.XunfeiASR()
        elif asr_slug == 'baidu-asr':
            asr = ASR.BaiduASR()
        else:
            asr = ASR.BaiduASR()
        return asr

    def do_TTS(self, tts_slug):
        global tts
        if tts_slug == 'baidu-tts':
            tts = TTS.BaiduTTS()
        elif tts_slug == 'xunfei-tts':
            tts = TTS.XunfeiTTS()
        else:
            tts = TTS.BaiduTTS()
        return tts
