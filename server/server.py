import tornado.ioloop
import tornado.web
import tornado.escape
import sys
from robot import config, logging, statistic
import threading
import asyncio
import json
import os
import yaml

conversation = None



class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):

    def get(self):
        global conversation
        if not self.current_user:
            self.redirect('/login')
            return
        self.render('index.html', history = conversation.getHistory())

class ConfigHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
            return
        self.render('config.html',config=config.getText())

    def post(self):
        if not self.current_user:
            res = {'code':1, 'message':'illegal visit'}
            self.write(json.dumps(res))
        else:
            configStr = self.get_argument('config')
            try:
                yaml.load(configStr, Loader=yaml.FullLoader)
                config.dump(configStr)
                res = {'code':0, 'message':'ok'}
                self.write(json.dumps(res))
            except:
                res = {'code': 1, 'message': 'YAML解析失败,请检查内容'}
                self.write(json.dumps(res))
            self.finish()

class LogHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
            return
        self.render('log.html',log=logging.readLog())

class HistoryHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            res = {'code':1, 'message':'illegal visit'}
        else:
            res = {'code':0, 'message':'ok', 'history':json.dumps(conversation.getHistory())}
        self.write(json.dumps(res))
        self.finish()

class GetLogHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            res = {'code':1, 'message':'illegal visit'}
        else:
            res = {'code':0, 'message':'ok', 'log':logging.readLog()}
        self.write(json.dumps(res))
        self.finish()

class ActiveHandler(BaseHandler):

    def get(self):
        count = []
        days = []
        if not self.current_user:
            self.redirect('/login')
            return
        else:
            dict = statistic.active()
            for d, c in dict.items():
                days.append(d)
                count.append(c)
                days = days[-10:]
                count = count[-10:]
        self.render('active.html',days = json.dumps(days), count = json.dumps(count))


class OperateHandler(BaseHandler):
    def post(self):
        if not self.current_user:
            res = {'code':1, 'message':'illegal visit'}
            self.write(json.dumps(res))
        else:
            res = {'code':0, 'message':'ok'}
            self.write(json.dumps(res))
            self.finish()
            python = sys.executable
            os.execl(python, python, *sys.argv)


class ChatHandler(BaseHandler):
    def post(self):
        if not self.current_user:
            res = {'code':1, 'message':'illegal visit'}
        else:
            query = self.get_argument('query', '')
            if query != '':
                conversation.doResponse(query)
            res = {'code':0, 'message':'ok'}
        self.write(json.dumps(res))
        self.finish()

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.render('/')
            return
        self.render('login.html')
    def post(self):
        if config.get('/server/password') == self.get_argument('password', default=''):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.write('登录失败!')
settings = {
    "cookie_secret":"\x0e8\xc4\xe1\xa8\\js\xa0\x05\xc4\x8c'\xf2\x93tkDT\x0b\x14\xfa\xc4\x87",
    "template_path":"server/templates",
    "static_path": "server/static",
    "debug": True,
}


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/login', LoginHandler),
        (r'/config', ConfigHandler),
        (r'/log', LogHandler),
        (r'/history', HistoryHandler),
        (r'/chat', ChatHandler),
        (r'/getlog', GetLogHandler),
        (r'/operate', OperateHandler),
        (r'/active', ActiveHandler),
    ], **settings)
app = make_app()
def start_server():
    # 创建一个新的IOloop,防止与悟空的发生冲突
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.listen(config.get('/server/port', 5000))
    tornado.ioloop.IOLoop.current().start()

def run(con):
    global conversation
    conversation = con
    threading.Thread(target=start_server).start()