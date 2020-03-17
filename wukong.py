from snowboy import snowboydecoder
import sys
import signal
from robot import Player, config, logging, TTS
from robot.Conversation import Conversation

logger = logging.getLogger(__name__)
"""
This demo file shows you how to use the new_message_callback to interact with
the recorded audio after a keyword is spoken. It uses the speech recognition
library in order to convert the recorded audio into text.
Information on installing the speech recognition library can be found at:
https://pypi.python.org/pypi/SpeechRecognition/
"""


interrupted = False
player = None



def audioRecorderCallback(fname):
    global player
    conversation = Conversation()
    conversation.converse(fname)



def detectedCallback():

    global player
    if player:
        player.stop()
    Player.player('static/beep_hi.wav', False)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# 更改唤醒词为配置文件中的值，默认为snowboy文件夹中的
model = config.get('/snowboy/hotword','snowboy/resources/jarvis.pmdl')

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=config.get('/snowboy/sensitivity', 0.38))
print('""""""""""""""""""""""""""""""'
      'robot'
      '"""""""""""""""""""""""""""""""')
Player.hello()
logger.info('Listening... Press Ctrl+C to exit')


# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()