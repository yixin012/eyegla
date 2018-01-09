# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os

import time
from datetime import datetime, timedelta
from config.mysql import conn

JDK_HOME = "/shiheng/sys/jdk/"
apps = [
    {
        'app_name': 'trade2',
        'server_name': '/shiheng/sys/jetty/',
        'ip': '127'
    }
]


SHELL_COMMAND_PID = 'ps -ef | grep java | grep "%s" | awk \'{print $2}\''
SHELL_COMMAND_CAPACITY = JDK_HOME + 'bin/jstat -gccapacity %s'


def collect_jvm_pid(app):
    server_name = app.get('server_name')

    command = SHELL_COMMAND_PID % server_name
    output = os.popen(command)
    s_pid = output.readlines()[0]
    pid = int(s_pid.strip())
    return pid

def collect_jvm_capacity(app, pid):
    '''
    jstat -gccapacity pid
    '''
    app_name = app.get('app_name')
    command = SHELL_COMMAND_CAPACITY % pid
    output = os.popen(command)
    row_data = output.readlines()

    name=row_data[0].split()
    value=row_data[1].split()
    all_dic=dict(zip(name,value))

    stime = datetime.now()

    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:%S"),
        'app': app_name,
        'ngcmn': all_dic.get('NGCMN'),
        'ngcmx': all_dic.get('NGCMX'),
        'ngc': all_dic.get('NGC'),
        's0c': all_dic.get('S0C'),
        's1c': all_dic.get('S1C'),
        'ec': all_dic.get('EC'),
        'ogcmn': all_dic.get('OGCMN'),
        'ogcmx': all_dic.get('OGCMX'),
        'ogc': all_dic.get('OGC'),
        'oc': all_dic.get('OC'),
        'mcmn': all_dic.get('MCMN'),
        'mcmx': all_dic.get('MCMX'),
        'mc': all_dic.get('MC'),
        'ccsmn': all_dic.get('CCSMN'),
        'ccsmx': all_dic.get('CCSMX'),
        'ccsc': all_dic.get('CCSC'),
        'ygc': all_dic.get('YGC'),
        'fgc': all_dic.get('FGC'),
        'ip': app.get('ip')
    }



def push_data_to_mysql(data):
    cur = conn.cursor()
    try:
        sql = '''insert into jvm_capacity(time, app,ip, ngcmn,ngcmx,ngc,s0c,s1c,ec,ogcmn,ogcmx,ogc,oc,mcmn,mcmx,mc,ccsmn,ccsmx,ccsc,ygc,fgc)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
        values = [(data.get('time'), data.get('app'), data.get('ip'),
                   float(data.get('ngcmn')),
                   float(data.get('ngcmx')),
                   float(data.get('ngc')),
                   float(data.get('s0c')),
                   float(data.get('s1c')),
                   float(data.get('ec')),
                   float(data.get('ogcmn')),
                   float(data.get('ogcmx')),
                   float(data.get('ogc')),
                   float(data.get('oc')),
                   float(data.get('mcmn')),
                   float(data.get('mcmx')),
                   float(data.get('mc')),
                   float(data.get('ccsmn')),
                   float(data.get('ccsmx')),
                   float(data.get('ccsc')),
                   int(data.get('ygc')),
                   int(data.get('fgc'))
                   )]
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

def collect_data():

    for app in apps:
        pid = collect_jvm_pid(app)
        j_capacity = collect_jvm_capacity(app, pid)

        push_data_to_mysql(j_capacity)

