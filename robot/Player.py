import subprocess
import os
import threading
from robot import utils,config,TTS

def hello():
    name = config.get('/name')
    phrase = '{}你好，我是贾维斯，试试对我喊唤醒词唤醒我吧'.format(name)
    tts = TTS.BaiduTTS()
    fp = tts.get_speech(phrase)
    SoxPlayer().play(fp, True)


def player(src, delete=False):
    # 将传递的录制的音频进行拆分
    foo, ext = os.path.splitext(src)
    # 如果属于这种格式，执行播放，参数为（内容，播放后是否删除）
    if ext in ('.wav', '.mp3'):
        player = SoxPlayer()
        player.play(src, delete)


# 创建一个线程的基类
class AbstrastPlayer(threading.Thread):

    def player(self, src):
        pass


# 继承基类来完成播放器的方法
class SoxPlayer(AbstrastPlayer):

    def __init__(self):
        # 首先执行init操作，将正在播放的变量设为False
        super(SoxPlayer, self).__init__()
        self.playing = False

    def run(self):
        cmd = ['play', self.src]
        # 播放,禁止打印播放的log
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        # 设置一个变量，如果为True则表示正在播放
        self.playing = True
        # 等待播放完成
        self.proc.wait()
        self.playing = False
        # 如果delete=True，并且该文件存在，则删除
        if self.delete:
            utils.check_and_delete(self.src)

    def play(self, src, delete=False):
        # 将变量写成成员变量
        self.src = src
        self.delete = delete
        # 执行子进程
        self.start()

    def stop(self):
        if self.proc and self.playing:
            # 结束子进程
            self.proc.terminate()
            if self.delete:
                utils.check_and_delete(self.src)
