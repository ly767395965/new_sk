#!/usr/bin/python3
import pymysql
import bConfig


class dbServer:
    db_config = ''

    def __init__(self):
        self.db_config = bConfig.getconfig()
        self.db_config = self.db_config['db_config']

    def dbConnect(self):
        host = self.db_config['host']
        user = self.db_config['user']
        pawss = self.db_config['pawss']
        database = self.db_config['database']
        return pymysql.connect(host, user, pawss, database)

    def executeSql(self, sql, where=()):  # 执行sql
        connect = self.dbConnect()
        cursor = connect.cursor()
        try:
            result = cursor.execute(sql, where)  # 执行sql时返回影响的行数, 查询sql 返回记录数
            connect.commit()
        except Exception as e:
            connect.rollback
            print(str(e))
            result = False

        connect.close()
        return result

    def querySql(self, sql, where=()):
        connect = self.dbConnect()
        cursor = connect.cursor()
        try:
            cursor.execute(sql, where)  # 执行sql时返回影响的行数
            desc = cursor.description
            connect.commit()
            result = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
            return result
        except Exception as e:
            connect.rollback
            print(str(e))
            result = False

        connect.close()
        return result

    def addData(self, table, data):
        if not len(data):
            return False

        sql = 'INSERT INTO ' + table
        fleds = ' ('
        add_val = ' ('
        for key, val in data.items():
            fleds += '`'+key+'`,'
            add_val += "'"+val+"',"

        fleds = fleds.rstrip(',')
        add_val = add_val.rstrip(',')
        sql += fleds + ') VALUE ' + add_val + ')'
        print(sql)
        connect = self.dbConnect()
        cursor = connect.cursor()
        try:
            result = cursor.execute(sql)  # 执行sql时返回影响的行数, 查询sql 返回记录数
            connect.commit()
        except Exception as e:
            connect.rollback
            print(str(e))
            result = False

        connect.close()
        return result

    def addMulti(self, table, data):  # 一次添加多个
        if not len(data) or table == '':
            return False

        sql = 'INSERT INTO ' + table + ' '
        fleds = '('
        add_val = '('
        num = 0
        for list in data:
            for key, val in list.items():
                key = str(key)
                val = str(val)
                if num == 0:
                    fleds += '`' + key + '`,'

                add_val += "'" + val + "',"

            add_val = add_val.rstrip(',')
            add_val += '),('
            num += 1

        fleds = fleds.rstrip(',')
        add_val = add_val.rstrip(',(')
        sql += fleds + ') VALUES ' + add_val
        return self.executeSql(sql)

    def updataAry(self, tab_name, data, where=''):
        sql = 'UPDATE ' + tab_name + ' SET '
        for key, val in data.items():
            key = str(key)
            val = str(val)
            sql += key + "='" + val + "',"

        sql = sql.rstrip(',')
        if where != '':
            sql += ' WHERE '+where

        return self.executeSql(sql)

    def delDate(self):
        print('db server delDate fun')

    def close(self):
        print('db server close fun')

