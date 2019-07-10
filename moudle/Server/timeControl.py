import time
import skOp
import db

class timeCtl():
    def __init__(self):
        self.dd_data = 0  # 日数据最后日期
        self.tt_data = 0  # 时数据最后时间

    def setTask(self):  # 设置任务
        print(12)

    def cyleData(self):  # 周期数据入口
        nowTime = time.strftime("%H:%M:%S", time.localtime())
        time_ary = nowTime.split(':')
        minute = time_ary[1]
        minute = int(minute)
        # if nowTime < '09:00:00' or nowTime > '15:15:00':  # 非时间内
        #     return 0
        # elif '11:45:00' < nowTime < '13:00:00':
        #     return 0

        skop_obj = skOp.skOpC()
        if nowTime > '19:05:00':
            return 4
        else:
            skop_obj.writeCycleDate('60')
            time.sleep(2)
            skop_obj.writeCycleDate('30')
            return 3

        return 1

    def writeSva(self):  # 写入均数据
        skop_obj = skOp.skOpC()
        skop_obj.opSva('30')
        skop_obj.opSva('60')

    def nowData(self):  # 即时数据获取,及下次触发时间返回
        print()



