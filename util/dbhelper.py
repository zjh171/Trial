from time import strftime

import pymysql.cursors

import model.trial

# 连接配置信息
from model import trial

config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '',
        'db': 'spda',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }


class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)
        return cls._instance


class DBHelper(Singleton):
    connection = ''

    def __init__(self):
        # 创建连接
        self.connection = pymysql.connect(**config)
        return None



    def selectAll(self):
        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'SELECT * FROM trial'
                cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()

            for resultItem in result:
                resultItem['start_date'] = (resultItem['start_date']).strftime('%Y-%m-%d')

            # print(result)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()
        finally:
            pass
            # self.connection.close()
        return result

    def selectTrial(self,trialId):
        result = None
        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'SELECT * FROM trial where trial_id=%s'
                cursor.execute(sql,trialId)
            # 获取查询结果
            result = cursor.fetchone()
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()

        finally:
            pass
        return result
    def updateTrial(self,trial):
        result = False
        try:
            with self.connection.cursor() as  cursor:
                sql = 'UPDATE trial SET medi_name= %s ,medi_sort = %s,trial_type = %s,reg_sort = %s,company_name = %s,start_date =%s  WHERE trial_id=%s'
                cursor.execute(sql,(trial.mediName,trial.mediSort,trial.trialType,trial.registerSort,trial.companyName,trial.startDate,trial.trialId))
                result = self.connection.commit()
                if(result):
                    result = True
        finally:
            pass
        return result

    def insertTrial(self,trial):
        result = self.selectTrial(trial.trialId)

        if(result):
            self.updateTrial(trial)
        else:
            try:
                with self.connection.cursor() as  cursor:
                    sql = 'INSERT INTO trial (trial_id, medi_name,medi_sort,trial_type,reg_sort,company_name,start_date) VALUES (%s, %s, %s,%s,%s,%s,%s)'
                    cursor.execute(sql, (trial.trialId, trial.mediName,trial.mediSort,trial.trialType,trial.registerSort,trial.companyName,trial.startDate))
                    self.connection.commit()
            finally:
                pass

    def close(self):
        self.connection.close()





