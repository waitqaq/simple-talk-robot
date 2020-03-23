from robot import logging,Conversation
import numpy as np

logger = logging.getLogger(__name__)

def active():
    global times, cuple
    list = []
    time_list = []
    days = []
    t_dict = {}
    l = []
    # 获取保存激活log里面的每一行
    logs = logging.read_active_log().splitlines()
    # 进行遍历取值,进行切片,保留后面的时间
    for log in logs:
        times = log.split(': ')[1]
        list.append(times)
    # 将时间进行切片,保留年月日,去掉时分秒
    for i in list:
        time =  i.split(' ')
        time_list.append(time)
    # 将年月日另存为一个列表
    for t_list in time_list:
        l.append(t_list[0])
    # 进行频数统计
    result = {}
    for i in np.unique(l):
        result[i] = l.count(i)
    """
    {'2020-03-10': 1, '2020-03-11': 1, '2020-03-12': 1, '2020-03-13': 1, '2020-03-14': 1, '2020-03-23': 33, '2020-03-25': 1, '2020-03-26': 1, '2020-03-27': 1, '2020-03-28': 1, '2020-03-29': 1, '2020-03-30': 1}
    """
    return result