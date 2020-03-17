from robot.sdk.AbstractPlugin import AbstractPlugin
import requests
from robot import logging,config

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):

    # 创建一个查询天气的技能
    def handle(self, query):
        logger.info('命中 <天气> 插件')
        city = config.get('/location')
        url = 'https://free-api.heweather.net/s6/weather/forecast?parameters'
        params = {
            "location": city,
            "key": 'b2cfbad4db8f4638a6d4fb221d4f2753'
        }
        r = requests.get(url, params=params)
        r.encoding= 'utf-8'
        try:
            results = r.json()['HeWeather6'][0]['daily_forecast']
            logger.debug(results)
            res = '{}天气'.format(city)
            day_label = ['今天','明天','后天']
            i=0
            for result in results:
                # 通过获取的json串分别获取最高气温，最低气温，白天气温，夜间气温
                tmp_min, tmp_max, cond_txt_d, cond_txt_n = \
                    result['tmp_min'],result['tmp_max'],result['cond_txt_d'],result['cond_txt_n']
                res += '{}：白天{}，夜间{}，气温{}度到{}度，'.format(day_label[i],cond_txt_d, cond_txt_n, tmp_max, tmp_min)
                i += 1
            self.con.say(res, True)
            logger.info(res)
        except Exception as e:
            logger.error(e)
            self.con.say("天气查询失败了！", True)

    def isValid(self, query):

        return '天气' in query