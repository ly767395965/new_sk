#!/usr/bin/python3


def getconfig():
    list = {
        'db_config': {
            'host': '127.0.0.1',
            'user': 'root',
            'pawss': '',
            'database': 'shares'
        },
        'redis': {
            'host': '127.0.0.1',
            'port': 6379
        },
        'get_sk': {
            'current_get': 'http://hq.sinajs.cn/list=',  # 新浪实时sk数据
            'cycle_get': 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?',  # 新浪周期数据
            'sk_type': ('sh', 'sz')  # 类型标识:上 sh; 深 sz
        }
    }
    return list

