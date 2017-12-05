# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os

import time
from datetime import datetime, timedelta
from config.mysql import conn


NGINX = {
    'app': 'nginx',
    'log_file': '/shiheng/logs/nginx/access.log'
}
NGINX_LOG_FORMAT = '%d/%b/%Y:%H:%M'
apps = [
    {
        'app_name': 'trade',
        'app_key': '127.0.0.1:8081'
    },
    {
        'app_name': 'trade2',
        'app_key': '127.0.0.1:8080'
    }
]


SHELL_COMMAND = 'grep "%s" %s | grep "%s" | wc -l'
SHELL_COMMAND_TYPE = 'grep "%s" %s | grep "%s" | grep "%s" | wc -l'


def collect_nginx_by_key(app, time_key):
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = NGINX.get('log_file')
    command = SHELL_COMMAND % (time_key, log_file, app_key)
    output = os.popen(command)
    num = output.readlines()[0]
    ss_num = int(num.strip())

    stime = datetime.strptime(time_key, NGINX_LOG_FORMAT)

    print command, ss_num
    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:00"),
        'app': app_name,
        'num': ss_num,
        'ip': '39.108.237.190'
    }

def collect_nginx_by_type(app, time_key, type):
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = NGINX.get('log_file')
    command = SHELL_COMMAND_TYPE % (time_key, log_file, app_key, type)
    output = os.popen(command)
    num = output.readlines()[0]
    ss_num = int(num.strip())

    stime = datetime.strptime(time_key, NGINX_LOG_FORMAT)

    print command, ss_num
    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:00"),
        'app': app_name+'-'+type,
        'num': ss_num,
        'ip': '39.108.237.190'
    }

def collect_data():
    now = datetime.now()
    ## 统计上一分钟
    first_min = now - timedelta(minutes=1)
    time_str = first_min.strftime('%d/%b/%Y:%H:%M')
    collect_data_by_date(time_str)


def collect_data_by_date(time):
    '''
    :param time: 'yyyy-mm-dd HH:MM'
    :return:
    '''
    datas = [collect_nginx_by_key(app, time) for app in apps]
    types = ['Android', 'iPhone']
    type_datas = [collect_nginx_by_type(apps[1], time, type) for type in types]
    push_data_to_mysql(datas, type_datas)

def push_data_to_mysql(datas, type_datas):
    cur = conn.cursor()
    try:
        sql = '''insert into nginx_num_m(time, app, num, ip)
                values(%s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
        values = [(data.get('time'), data.get('app'), int(data.get('num')), data.get('ip')) for data in datas]
        cur.executemany(sql,values)

        type_sql = '''insert into nginx_num_type(time, app, num, ip)
                values(%s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
        types_values = [(data.get('time'), data.get('app'), int(data.get('num')), data.get('ip')) for data in type_datas]
        cur.executemany(type_sql, types_values)

    except Exception,ex:
        print ex
        return False
    finally:
        conn.commit()

        cur.close()
        conn.close()
    #print values
    return True


