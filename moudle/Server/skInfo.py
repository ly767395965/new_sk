#!/usr/bin/python3
import time
import db
# sk 数据查询
class skInfo:
    def getSkBase(self, sk_id, field='*'):  # 根据sk_id 获取sk base
        sql = "SELECT "+field+" FROM share_indexes_tab WHERE id=%s"
        db_server = db.dbServer()
        ressult = db_server.querySql(sql, sk_id)
        if ressult:
            return ressult[0]
        return False

    # 获取sk某天的详细信息
    # tab_num 表序号
    # start_t stop_t 开始时间或结束时间 格式 2019-01-22 16:26:23  默认当天00:00:00  到 59:59:59
    def getSkDetailed(self, tab_num, sk_id, date, field='*'):
        sk_tab = 'shares_data' + tab_num
        sql = "SELECT "+field+" FROM "+sk_tab+" WHERE share_id = "+sk_id+" AND date='"+date+"' ORDER BY id DESC"
        db_server = db.dbServer()
        ressult = db_server.querySql(sql)
        return ressult

    def getAllMonitor(self):  # 获取所有监控sk base
        db_server = db.dbServer()
        sql = 'SELECT id,share_code,share_type,data_tab FROM share_indexes_tab WHERE is_monitor = 1 AND is_del=0'
        ressult = db_server.querySql(sql)
        return ressult

    def getAllSkBase(self):  # 获取所有sk base
        db_server = db.dbServer()
        sql = 'SELECT id,share_code,share_type,data_tab FROM share_indexes_tab WHERE is_del=0'
        ressult = db_server.querySql(sql)
        return ressult

    def getSkLine(self, sk_id, scale='30'):  # 获取sk线性数据
        db_server = db.dbServer()
        tab_name = 'price_'+scale+'min'
        sk_id = str(sk_id)
        sql = "SELECT COUNT(id) as num FROM "+tab_name+" WHERE share_id="+sk_id+" AND status = 0"
        num_c = db_server.querySql(sql)
        if not num_c:
            return False

        num_c = str(num_c[0][0] + 60)

        sql = 'SELECT id, endPri, status FROM '+tab_name+' WHERE share_id='+sk_id+' ORDER BY date DESC LIMIT '+num_c
        ressult = db_server.querySql(sql)
        return ressult

    def getCyclelist(self):
        db_server = db.dbServer()
        sql = 'SELECT * FROM price_30min WHERE share_id= 1 ORDER BY id DESC '
        ressult = db_server.querySql(sql)
        return ressult

    def getDateskInfo(self, date='', tab_num=2):  # 获取某天sk信息,默认当天的数据
        db_server = db.dbServer()
        sql = "SELECT * FROM shares_data2 WHERE share_id=3 AND `time`='15:00:00' ORDER BY id DESC"
        ressult = db_server.querySql(sql)
        return ressult

    def getMinInfo(self):
        db_server = db.dbServer()
        sql = "SELECT * FROM shares_data2 WHERE share_id=3 AND `date`='2019-05-30' ORDER BY id DESC "
        ressult = db_server.querySql(sql)
        return ressult

    def getMinInfo2(self):
        db_server = db.dbServer()
        sql = "SELECT * FROM (SELECT *, FROM_UNIXTIME(UNIX_TIMESTAMP(`time`),'%H:%i') as g_time FROM shares_data2 WHERE share_id=5 AND `date`='2019-04-18'ORDER BY id DESC ) GROUP BY g_time"
        ressult = db_server.querySql(sql)
        return ressult

    def insertCycle(self, data, scale='30'):  # 插入周期数据
        tab_name = 'price_'+scale+'min'
        db_server = db.dbServer()

        add_data = []
        up_data = []
        up_where = []
        for key, val in data.items():
            val['share_id'] = str(val['share_id'])
            where = "share_id="+val['share_id']+" AND date = '"+val['date']+"'"
            sql = "SELECT startPri, endPri, max, min, traNumber FROM "+tab_name+" WHERE "+where
            res = db_server.querySql(sql)
            if not res:
                add_data.append(val)  # 去数据库查看是否存在,如果不存在插入改记录, 后期可改成去redis中查询
            else:
                old_list = res[0]
                if val['startPri'] != old_list[0] or val['endPri'] != old_list[1] or val['max'] != old_list[2] or val['min'] != old_list[3] or val['traNumber'] != old_list[4]:
                    up_data.append(val)
                    up_where.append(where)

        if len(add_data) != 0:
            db_server.addMulti(tab_name, add_data)
        elif len(up_data) != 0:
            key = 0
            for val in up_data:
                db_server.updataAry(tab_name, val, up_where[key])
                key += 1

        return True

    def upSva(self, data, scale):  # 更新均值到数据库
        db_server = db.dbServer()
        tab_name = 'price_'+scale+'min'
        for key, val in data.items():
            where = 'id = ' + key
            cont = val['count']
            del val['count']
            if cont < 60:
                del val['60avg_num']
            else:
                val['60avg_num'] /= 60

            if cont < 20:
                del val['20avg_num']
            else:
                val['20avg_num'] /= 20

            if cont < 10:
                del val['10avg_num']
            else:
                val['10avg_num'] /= 10

            if cont < 5:
                del val['5avg_num']
            else:
                val['5avg_num'] /= 5

            db_server.updataAry(tab_name, val, where)

        return True

    def interNowData(self, sk_base, sk_info, type=0):  # 插入now data
        db_server = db.dbServer()
        if type == 0:
            tmp_name = 'shares_data'
        else:
            tmp_name = 'shares_min'

        now_time = int(time.time())
        for val in sk_base:
            share_code = val['share_code']
            if share_code in sk_info:
                tab_name = tmp_name+str(val['data_tab'])
                info = sk_info[share_code]
                data_ary = info.split(',')
                nowPri = float(data_ary[3])
                yestodEndPri = float(data_ary[2])
                increPer = (nowPri-yestodEndPri) /yestodEndPri
                increPer = round(increPer * 100, 2)
                list = {}
                list['share_id'] = val['id']
                list['increPer'] = increPer
                list['increase'] = nowPri -yestodEndPri
                list['todayStartPri'] = data_ary[1]
                list['yestodEndPri'] = data_ary[2]
                list['nowPri'] = data_ary[3]
                list['todayMax'] = data_ary[4]
                list['todayMin'] = data_ary[5]
                list['competitivePri'] = data_ary[6]
                list['reservePri'] = data_ary[7]
                list['traAmount'] = data_ary[9]
                list['traNumber'] = data_ary[8]
                list['buyOne'] = data_ary[10]
                list['buyOnePri'] = data_ary[11]
                list['buyTwo'] = data_ary[12]
                list['buyTwoPri'] = data_ary[13]
                list['buyThree'] = data_ary[14]
                list['buyThreePri'] = data_ary[15]
                list['buyFour'] = data_ary[16]
                list['buyFourPri'] = data_ary[17]
                list['buyFive'] = data_ary[18]
                list['buyFivePri'] = data_ary[19]
                list['sellOne'] = data_ary[20]
                list['sellOnePri'] = data_ary[21]
                list['sellTwo'] = data_ary[22]
                list['sellTwoPri'] = data_ary[23]
                list['sellThree'] = data_ary[24]
                list['sellThreePri'] = data_ary[25]
                list['sellFour'] = data_ary[26]
                list['sellFourPri'] = data_ary[27]
                list['sellFive'] = data_ary[28]
                list['sellFivePri'] = data_ary[29]
                list['date'] = data_ary[30]
                list['time'] = data_ary[31]
                list['add_time'] = now_time

                sql = "SELECT id FROM " + tab_name + " WHERE `date`='"+list['date']+"' AND `time`='"+list['time']+"'"
                check_exist = db_server.querySql(sql)  # 检测数据库中是否存在, 如存在的话则不插入
                if check_exist:
                    continue

                db_server.addData(tab_name, list)

        return True
