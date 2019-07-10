#!/usr/bin/python3
import requests
import skInfo
import skData
import bConfig
import redisOp

# sk 操作类
class skOpC:
    def writeDateData(self):  # 写入每日数据
        print()

    def writeCycleDate(self, scale='30'):  # 写入周期数据
        skinfo_obj = skInfo.skInfo()
        sk_list = skinfo_obj.getAllSkBase()  #0:id, 1:sk_code 2:sk_type
        skdata_obj = skData.skData()

        sk_num = len(sk_list)
        if sk_num == 0:
            return {'code': 501, 'msg': '数据库中正常sk为空!'}

        for val in sk_list:
            http_res = self.getCycleDate(val[1], val[2], scale)  # 获取单个sk 周期信息
            if not http_res:
                print(val[0]+':获取'+scale+'周期数据异常')
                continue

            res = skdata_obj.analysisCycleData(http_res)  # 返回数据进行序列化
            if not res:
                print(val[0]+':'+scale+'周期数据分析异常, '+http_res)
                continue

            res = skdata_obj.assembleCycle(res, val[0])  # 组装插入数据
            res = skinfo_obj.insertCycle(res, scale)  # 进行数据插入
            if not res:
                print(val[0] + ':' + scale + '数据插入异常异常')

    def opSva(self, scale='30'):  # 计算sva数据
        skinfo_obj = skInfo.skInfo()
        sk_list = skinfo_obj.getAllSkBase()  # 0:id, 1:sk_code 2:sk_type
        skdata_obj = skData.skData()

        for val in sk_list:
            sk_id = val[0]
            sk_line = skinfo_obj.getSkLine(sk_id, scale)  # 获取线性数据
            if not sk_line:
                print(str(sk_id) + ':' + scale + '未查找到线性数据')

            sva = skdata_obj.getAvgVal(sk_line)  # 计算均值
            skinfo_obj.upSva(sva, scale)  # 更新数据库

        return True

    def getNowData(self, type=1):
        # test = 'var hq_str_sh000001="fdsafsaf"fdsf'
        # first_l = test.find('"')
        # print(first_l)
        # print(test[first_l-7:first_l-1])
        # return
        skinfo_obj = skInfo.skInfo()
        sk_list = skinfo_obj.getAllSkBase()  # 0:id, 1:sk_code 2:sk_type
        data = self.getImmediateData(sk_list)
        skdata_obj = skData.skData()

        sk_anlys = skdata_obj.analysisImmediateData(data)
        skinfo_obj.interNowData(sk_list, sk_anlys, type)

    def getCycleDate(self, sk_code, sk_t, scale='60', len='3'):  # 获取周期数据 每次只能获取一个sk数据  len 经测试的最大值192
        config = bConfig.getconfig()
        sk_config = config['get_sk']
        url = sk_config['cycle_get']
        sk_type = sk_config['sk_type']
        url += 'symbol='+sk_type[sk_t] + sk_code + '&scale='+scale + '&ma=no&datalen='+len
        res = requests.get(url)
        return res.text

    def getImmediateData(self, sks_ary):  # 获取实时数据 可获取多个sk数据
        config = bConfig.getconfig()
        sk_config = config['get_sk']
        url = sk_config['current_get']
        sk_type = sk_config['sk_type']

        for val in sks_ary:
            sk_t = val['share_type']
            sk_t = int(sk_t)
            url += sk_type[sk_t]+val['share_code']+','

        res = requests.get(url)
        return res.text

    def dateAnalysis(self):  # everyday
        skinfo_obj = skInfo.skInfo()
        list = skinfo_obj.getMinInfo()
        len_num = len(list)
        tmp = {}
        first_l = []
        for key in range(len_num):
            if key == 0:
                continue

            new_d = list[key-1]
            old_d = list[key]
            diff_z = new_d['increPer'] - old_d['increPer']
            if len(tmp) == 0:
                if diff_z > 0:
                    tmp = self.inittmp(new_d, 1)
                elif diff_z < 0:
                    tmp = self.inittmp(new_d, 0)
                else:
                    continue

            else:
                if diff_z == 0 or (diff_z > 0 and tmp['direction'] == 1) or (diff_z < 0 and tmp['direction'] == 0):
                    tmp['count'] += 1
                    continue

                tmp['start_time'] = new_d['time']
                tmp['start_z'] = new_d['increPer']
                tmp['start_time_s'] = new_d['add_time']
                first_l.append(tmp)

                if diff_z > 0 and tmp['direction'] == 0:
                    tmp = self.inittmp(new_d, 1)

                if diff_z < 0 and tmp['direction'] == 1:
                    tmp = self.inittmp(new_d, 0)

        data = self.filterData(first_l)
        if len(data) > 0:
            key = 'share_min_per:share_code'
            robj = redisOp.redisOp()
            redis = robj.getRedis()
            val = data[0]
            per = round(val['per'], 3)
            redis.set(key, per)

        return data

    def inittmp(self, new_d, dir):
        tmp = {}
        tmp['direction'] = dir
        tmp['now_z'] = new_d['increPer']
        tmp['now_time'] = new_d['time']
        tmp['now_time_s'] = new_d['add_time']
        tmp['count'] = 1
        return tmp

    def filterData(self, data):
        tmp = {}
        down_tmp = []
        yesterday_pri = 9.58
        two_points_per = 0.23

        for val in data:
            per = val['now_z'] - val['start_z']
            per_abs = abs(per)
            if len(tmp) == 0:   # 如果tmp为空则进行初始化
                tmp['now'] = val['now_z']
                tmp['start_z'] = val['start_z']
                tmp['now_time'] = val['now_time']
                tmp['start_time'] = val['start_time']
                tmp['per'] = per
                if val['direction'] == 0:
                    tmp['max'] = val['start_z']
                    tmp['min'] = val['now_z']
                else:
                    tmp['max'] = val['now_z']
                    tmp['min'] = val['start_z']
                if per_abs > two_points_per:
                    tmp['direction'] = val['direction']
                    tmp['big_wave'] = 1
                    tmp['wave'] = 0
                else:
                    tmp['wave'] = 1
                    tmp['big_wave'] = 0

            else:
                is_direc = per * tmp['per']  # 判断是否同向, 正数同向,负数反向

                if per_abs > two_points_per:
                    if 'direction' in tmp and is_direc < 0:
                        down_tmp.append(tmp)
                        tmp = {}
                        tmp['now'] = val['now_z']
                        tmp['start_z'] = val['start_z']
                        tmp['now_time'] = val['now_time']
                        tmp['start_time'] = val['start_time']
                        tmp['per'] = per
                        if val['direction'] == 0:
                            tmp['max'] = val['start_z']
                            tmp['min'] = val['now_z']
                        else:
                            tmp['max'] = val['now_z']
                            tmp['min'] = val['start_z']
                        tmp['direction'] = val['direction']
                        tmp['big_wave'] = 1
                        tmp['wave'] = 0

                    else:
                        tmp['per'] += per
                        tmp['big_wave'] += 1
                        tmp['start_z'] = val['start_z']
                        tmp['start_time'] = val['start_time']
                        if tmp['min'] > val['start_z']:
                            tmp['min'] = val['start_z']

                        if tmp['max'] < val['start_z']:
                            tmp['max'] = val['start_z']
                        if not ('direction' in tmp):
                            tmp['direction'] = val['direction']
                else:
                    tmp['per'] += per
                    tmp['wave'] += 1
                    tmp['start_z'] = val['start_z']
                    tmp['start_time'] = val['start_time']
                    if tmp['min'] > val['start_z']:
                        tmp['min'] = val['start_z']

                    if tmp['max'] < val['start_z']:
                        tmp['max'] = val['start_z']

        return down_tmp

    def timeDiff(self, start_time, stop_time):  # 计算时间差
        start_ary = start_time.split(':')
        stop_ary = stop_time.split(':')
        h_d = int(stop_ary[0]) - int(start_ary[0])
        i_d = int(stop_ary[1]) - int(start_ary[1])
        s_d = int(stop_ary[2]) - int(start_ary[2])

        s_d += i_d * 60 + h_d * 3600
        return s_d

    def bsCheck(self, data):
        print()

