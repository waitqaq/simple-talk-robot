from robot.sdk.AbstractPlugin import AbstractPlugin
import requests
from robot import logging, config
import time

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):
    # 创建一个查询新冠疫情的技能
    def handle(self, query):
        province = config.get('/Covid/province')
        if '疫情情况' in query:
            logger.info('命中 <疫情情况> 插件')
            try:
                # 所在省份的患病相关人数情况
                url_num = 'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province=陕西省'
                data_num = requests.get(url=url_num)
                # 累计确诊人数
                confirmedCount = data_num.json()["results"][0]['confirmedCount']
                # 治愈人数
                curedCount = data_num.json()["results"][0]['curedCount']
                updateTime = (data_num.json()["results"][0]['updateTime'])/1000
                date = time.localtime(updateTime)  # 利用localtime()转换为时间数组
                format_date = time.strftime('%Y-%m-%d %H:%M:%S', date)  # 利用strftime()将其格式化为需要的格式

                res = '截止'+str(format_date)+','+province+'累计确诊人数'+str(confirmedCount)+'例,'+'治愈人数'+str(curedCount)+'例'
                self.con.say(res, True)
                logger.info(res)
            except Exception as e:
                logger.error(e)
                self.con.say("疫情情况查询失败了！", True)

        elif '疫情新闻' in query:
            logger.info('命中 <疫情新闻> 插件')
            try:
                # 这里由于处过重点省份外，其他省份新闻的信息性不高，所以采用全国新闻
                # 全国性质的新闻
                url_msg = 'http://lab.isaaclin.cn/nCoV/api/overall'
                msgs = requests.get(url=url_msg)
                # 新闻的标题（考虑到内容过长，影响体验，使用标题进行播报）
                msg = msgs.json()["results"][0]["generalRemark"]
                uptime = (msgs.json()["results"][0]["updateTime"])/1000
                date = time.localtime(uptime)  # 利用localtime()转换为时间数组
                format_date = time.strftime('%Y-%m-%d ', date)  # 利用strftime()将其格式化为需要的格式
                msgs = format_date + '新闻：'+msg
                self.con.say(msgs, True)
                logger.info(msgs)
            except Exception as e:
                logger.error(e)
                self.con.say("疫情新闻查询失败了！", True)
        else:
            logger.error('疫情情况获取失败了！')
            self.con.say("疫情情况获取失败了！", True)



    def isValid(self, query):
        return '疫情' in query