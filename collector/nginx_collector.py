# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os

import time
from datetime import datetime, timedelta
from config.mysql import conn


NGINX_LOG_FORMAT = '%d/%b/%Y:%H:%M'

nginx = {
    'ip': '39.108.237.190',
    'log_file': '/shiheng/logs/nginx/access.log',
    'apps': [
        {
            'app_name': 'trade',
            'app_key': '127.0.0.1:8081',
            'collect_type': False,
            'collect_ip': False,
            'collect_avg_time': False,
        },
        {
            'app_name': 'trade2',
            'app_key': '127.0.0.1:8080',
            'collect_type': True,
            'collect_ip': True,
            'collect_avg_time': True
        }
    ]
}

'''
log_format  main  '$remote_addr [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                        '$upstream_addr $upstream_response_time $request_time '
                      '"$http_user_agent" "$http_x_forwarded_for"';
grep "26/Jan/2018:22:11" /shiheng/logs/nginx/access.log | grep "127.0.0.1:8080" | awk '{sum+=$12*1000} END {print sum/NR}'
'''

SHELL_COMMAND = 'grep "%s" %s | grep "%s" | wc -l'
SHELL_COMMAND_TYPE = 'grep "%s" %s | grep "%s" | grep "%s" | wc -l'
SHELL_COMMAND_IP = 'grep "%s" %s | grep "%s" | awk \'{print $1}\' | sort | uniq | wc -l'

SHELL_COMMAND_REQUEST_TIME_AVG = "grep %s %s | grep %s | awk '{sum+=$12*1000} END {print sum/NR}'"


def collect_nginx_by_app(app, time_key):
    '''
    app 访问数量
    '''
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = nginx.get('log_file')
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
        'ip': nginx.get('ip')
    }

def collect_nginx_by_type(app, time_key, type):
    '''
    不同类型[android,ios]对app的访问数量
    '''
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = nginx.get('log_file')
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
        'ip': nginx.get('ip')
    }

def collect_nginx_by_ip(app, time_key):
    '''
    对app的访问ip的数量
    '''
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = nginx.get('log_file')
    command = SHELL_COMMAND_IP % (time_key, log_file, app_key)
    output = os.popen(command)
    num = output.readlines()[0]
    ss_num = int(num.strip())

    stime = datetime.strptime(time_key, NGINX_LOG_FORMAT)

    print command, ss_num
    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:00"),
        'app': app_name,
        'num': ss_num,
        'ip': nginx.get('ip')
    }

def collect_request_time_avg(app, time_key):
    '''
    对app的访问ip的数量
    '''
    app_name = app.get('app_name')
    app_key = app.get('app_key')
    log_file = nginx.get('log_file')
    command = SHELL_COMMAND_REQUEST_TIME_AVG% (time_key, log_file, app_key)
    output = os.popen(command)
    num = output.readlines()[0]
    ss_num = float(num.strip())

    stime = datetime.strptime(time_key, NGINX_LOG_FORMAT)

    print command, ss_num
    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:00"),
        'app': app_name,
        'num': ss_num,
        'ip': nginx.get('ip')
    }


def push_data_to_mysql(datas, type_datas, ip_datas, avg_time_datas):
    cur = conn.cursor()
    try:
        sql = '''insert into nginx_num_m(time, app, num, ip)
                values(%s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
        values = [(data.get('time'), data.get('app'), int(data.get('num')), data.get('ip')) for data in datas]
        cur.executemany(sql,values)

        if type_datas:
            type_sql = '''insert into nginx_num_type(time, app, num, ip)
                    values(%s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            types_values = [(data.get('time'), data.get('app'), int(data.get('num')), data.get('ip')) for data in type_datas]
            cur.executemany(type_sql, types_values)

        if ip_datas:
            ip_sql = '''insert into nginx_num_ip(time, app, num, ip)
                    values(%s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            ip_values = [(data.get('time'), data.get('app'), int(data.get('num')), data.get('ip')) for data in ip_datas]
            cur.executemany(ip_sql, ip_values)

        if avg_time_datas:
            atime_sql = '''insert into nginx_request_time_avg(time, app, num, ip)
                    values(%s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            atime_values = [(data.get('time'), data.get('app'), float(data.get('num')), data.get('ip')) for data in avg_time_datas]
            cur.executemany(atime_sql, atime_values)

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
    :param time: 'yyyy-mm-dd HH:MM'
    :return:
    '''
    types = ['Android', 'iPhone']
    apps = nginx.get('apps')
    datas = [collect_nginx_by_app(app, time) for app in apps]
    type_datas = []
    ip_datas = []
    atime_datas = []
    for app in apps:
        collect_type = app.get('collect_type')
        collect_ip = app.get('collect_ip')
        collect_atime = app.get('collect_avg_time')
        if collect_type:
            types = [collect_nginx_by_type(app, time, type) for type in types]
            type_datas.extend(types)

        if collect_ip:
            ip_data = collect_nginx_by_ip(app, time)
            ip_datas.append(ip_data)

        if collect_atime:
            atime_data = collect_request_time_avg(app, time)
            atime_datas.append(atime_data)

    push_data_to_mysql(datas, type_datas, ip_datas, atime_datas)


def collect_data():
    now = datetime.now()
    ## 统计上一分钟
    first_min = now - timedelta(minutes=1)
    time_str = first_min.strftime('%d/%b/%Y:%H:%M')
    collect_data_by_date(time_str)
