#!/usr/bin/python3
import time


# 日期转换为时间戳
# format 需要解析的日期格式 默认 '%Y-%m-%d %H:%M:%S'
def dateToTimeStamp(date, date_format=''):
    if format == '':
        date_format = '%Y-%m-%d %H:%M:%S'

    time_array = time.strptime(date, date_format)
    time_stamp = int(time.mktime(time_array))
    return time_stamp



