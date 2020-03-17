import requests
import time
import hashlib
import base64
from robot import utils
# 生成唯一的mac地址
from uuid import getnode as get_mac
import json


class AbstractRobot(object):

    def chat(self, query):
        pass


class TulingRobot(AbstractRobot):
    SULG = "tuling-robot"

    def __init__(self):
        self.api_key = "952d9c0c474d4bd297ea07cd2de64bfc"


    def chat(self, query):
        #  合成webapi接口地址
        URL = "http://openapi.tuling123.com/openapi/api/v2"
        params = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": query
                },
            },
            "userInfo": {
                "apiKey": "952d9c0c474d4bd297ea07cd2de64bfc",
                # 文档要求不超过32位，进行切片
                "userId": str(get_mac())[:32]
            }
        }
        # 发送post请求，进行参数传递
        r = requests.post(URL, data=json.dumps(params))
        r.encoding = 'utf-8'
        res = r.json()
        # 为了防止返回json出错，进行兜底
        try:
            # 获取返回json串的reuslt的值
            results = res['results']
            # 进行遍历取值
            for result in results:
                # 如果type位text，则打印出value的text的值
                if result['resultType'] == 'text':
                    return result['values']['text']
            return ''
        except Exception as e:
            print(e)
            return ''


