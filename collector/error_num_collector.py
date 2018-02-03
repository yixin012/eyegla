# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os

import time
import datetime
from config.mysql import conn

apps = [
    {
        'app': 'trade',
        'ip': '39.108.237.190',
        'log_file': '/shiheng/logs/app/trade/error.log'
    },
    {
        'app': 'trade2',
        'ip': '39.108.237.190',
        'log_file': '/shiheng/logs/app/trade2/error.log'
    }
]


SHELL_COMMAND = 'grep "%s" %s | wc -l'

def collect_trade_num_by_key(app, key):
    '''
    收集trade 异常数量
    :return:
    '''
    app_name = app.get('app')
    log_file = app.get('log_file')
    ip = app.get('ip')

    command = SHELL_COMMAND % (key, log_file)

    output = os.popen(command)
    num = output.readlines()[0]
    err_num = int(num.strip())
    print command, err_num

    return {
        'time': key +':00',
        'app': app_name,
        'err_num': err_num,
        'ip': ip
    }

def push_data_to_mysql(datas):
    cur = conn.cursor()
    try:
        sql = '''insert into err_num(stime, app, num, ip)
                values(%s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE stime=VALUES(stime) and app=VALUES(app) and ip=VALUES(ip)'''
        values = [(data.get('time'), data.get('app'), int(data.get('err_num')), data.get('ip')) for data in datas]
        # print values
        # for f in favorites: datetime.datetime.strptime(fav.get( 'created_date'),'%Y-%m-%dT%H:%M:%S'
        #     if not f.get('album_owner_id'):
        #         print f
        cur.executemany(sql,values)
    except Exception,ex:
        print ex
        return False
    finally:
        conn.commit()

        cur.close()
        conn.close()
    #print values
    return True


def collect_data_by_date(time):
    '''
    提取这一分钟的错误数
    :param time: 'yyyy-mm-dd HH:MM'
    :return:
    '''
    data = [collect_trade_num_by_key(app, time) for app in apps]
    push_data_to_mysql(data)


def collect_data():
    now = datetime.datetime.now()
    ## 统计上一分钟
    first_min = now - datetime.timedelta(minutes=1)
    time_str = first_min.strftime('%Y-%m-%d %H:%M')

    collect_data_by_date(time_str)

