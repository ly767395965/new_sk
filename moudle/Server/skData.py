#!/usr/bin/python3
import time

# sk数据处理类

class skData:
    def analysisImmediateData(self, data):  # 分解now data
        if len(data) < 30:
            return {'code': 501, 'msg': 'Insufficient data length'}  # 数据长度不足

        data_ary = data.split(';')
        sk_info = {}
        for val in data_ary:
            if len(val) < 30:
                print('未获取到该code信息')
            else:
                first_l = val.find('"')  # 查找 " 第一次出现的位置
                second_l = val.find('"', first_l+1)  # 查找 " 第二次出现位置
                tmp_key = val[first_l-7:first_l-1]  # 截取编号
                sk_info[tmp_key] = val[first_l:second_l-1]  # 截取中间的字符串

        return sk_info

    def analysisCycleData(self, data):  # 分解cycle data
        if data is None:
            return False

        data = data.lstrip('[')
        data = data.rstrip(']')
        data_ary = data.split('},')
        re_list = {}
        key = 0
        print(data_ary)
        for val in data_ary:
            val = val.lstrip('{')
            val = val.rstrip('}')
            val_ary = val.split(',')
            tmp = {}
            for dd in val_ary:
                dd_ary = dd.split(':"')
                tmp[dd_ary[0]] = dd_ary[1].rstrip('"')

            re_list[key] = tmp
            key += 1

        return re_list

    def assembleCycle(self, data, sk_id):  # 组装周期插入数据
        new_list = {}
        l_key = 0
        for key in data:
            val = data[key]
            tmp = {}
            tmp['share_id'] = sk_id
            tmp['startPri'] = val['open']
            tmp['endPri'] = val['close']
            tmp['max'] = val['high']
            tmp['min'] = val['low']
            tmp['traNumber'] = val['volume']
            tmp['date'] = val['day']

            new_list[l_key] = tmp
            l_key += 1

        return new_list

    def getAvgVal(self, data):  # 计算均值
        len_n = len(data)
        data_any = {}
        key = -len_n
        for val in data:  # 计算各均值
            r_val = data[key]
            line_id = str(r_val[0])
            if r_val[2] == 0:
                data_any[line_id] = {}
                data_any[line_id]['count'] = 0
                if key < -1:
                    tprice = r_val[1]
                    qprice = data[key+1][1]
                    data_any[line_id]['increase'] = tprice - qprice
                    data_any[line_id]['increPer'] = (data_any[line_id]['increase'] / qprice) * 100

                if key-2 >= -len_n:
                    data_any[line_id]['status'] = 1
                else:
                    data_any[line_id]['status'] = 0

            for d_key, d_val in data_any.items():
                d_val['count'] += 1
                count = d_val['count']
                if count > 60:
                    continue
                if d_val.__contains__('60avg_num'):
                    d_val['60avg_num'] += r_val[1]
                else:
                    d_val['60avg_num'] = r_val[1]

                if count > 20:
                    continue
                if d_val.__contains__('20avg_num'):
                    d_val['20avg_num'] += r_val[1]
                else:
                    d_val['20avg_num'] = r_val[1]

                if count > 10:
                    continue
                if d_val.__contains__('10avg_num'):
                    d_val['10avg_num'] += r_val[1]
                else:
                    d_val['10avg_num'] = r_val[1]

                if count > 5:
                    continue
                if d_val.__contains__('5avg_num'):
                    d_val['5avg_num'] += r_val[1]
                else:
                    d_val['5avg_num'] = r_val[1]

            key += 1

        return data_any

