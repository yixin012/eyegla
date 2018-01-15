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
        'server_home': '/shiheng/sys/jetty/',
        'pid_file': '/shiheng/sys/jetty/run/jetty.pid',
        'ip': '39.108.237.190',
        'collect_gc': True,
        'collect_capacity': False,
        'collect_thread_count': True
    }
]

SHELL_COMMAND_PID = 'cat %s'
SHELL_COMMAND_CAPACITY = JDK_HOME + 'bin/jstat -gccapacity %s'
SHELL_COMMAND_GC = JDK_HOME + 'bin/jstat -gc %s'
SHELL_COMMAND_THREAD = JDK_HOME + 'bin/jstack %s | grep tid= | wc -l'

def collect_jvm_pid(app):
    pid_file = app.get('pid_file')

    command = SHELL_COMMAND_PID % pid_file
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

def collect_jvm_gc(app, pid):
    '''
    jstat -gc pid
    '''
    app_name = app.get('app_name')
    command = SHELL_COMMAND_GC % pid
    output = os.popen(command)
    row_data = output.readlines()

    name=row_data[0].split()
    value=row_data[1].split()
    all_dic=dict(zip(name,value))

    stime = datetime.now()

    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:%S"),
        'app': app_name,
        's0c': all_dic.get('S0C'),
        's1c': all_dic.get('S1C'),
        's0u': all_dic.get('S0U'),
        's1u': all_dic.get('S1U'),
        'ec': all_dic.get('EC'),
        'eu': all_dic.get('EU'),
        'oc': all_dic.get('OC'),
        'ou': all_dic.get('OU'),
        'mc': all_dic.get('MC'),
        'mu': all_dic.get('MU'),
        'ccsc': all_dic.get('CCSC'),
        'ccsu': all_dic.get('CCSU'),
        'ygct': all_dic.get('YGCT'),
        'fgct': all_dic.get('FGCT'),
        'ygc': all_dic.get('YGC'),
        'fgc': all_dic.get('FGC'),
        'ip': app.get('ip')
    }

def collect_jvm_thread_count(app, pid):
    '''
    jstat -gc pid
    '''
    app_name = app.get('app_name')
    command = SHELL_COMMAND_THREAD % pid
    output = os.popen(command)
    num = output.readlines()[0]
    thread_count = int(num.strip())
    stime = datetime.now()

    return {
        'time': stime.strftime("%Y-%m-%d %H:%M:%S"),
        'app': app_name,
        'count': thread_count,
        'ip': app.get('ip')
    }


def push_data_to_mysql(gc_data, capacity_data, thread_count_data):
    cur = conn.cursor()
    try:
        if capacity_data:
            sql = '''insert into jvm_capacity(time, app,ip, ngcmn,ngcmx,ngc,s0c,s1c,ec,ogcmn,ogcmx,ogc,oc,mcmn,mcmx,mc,ccsmn,ccsmx,ccsc,ygc,fgc)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            values = [(capacity_data.get('time'), capacity_data.get('app'), capacity_data.get('ip'),
                       float(capacity_data.get('ngcmn')),
                       float(capacity_data.get('ngcmx')),
                       float(capacity_data.get('ngc')),
                       float(capacity_data.get('s0c')),
                       float(capacity_data.get('s1c')),
                       float(capacity_data.get('ec')),
                       float(capacity_data.get('ogcmn')),
                       float(capacity_data.get('ogcmx')),
                       float(capacity_data.get('ogc')),
                       float(capacity_data.get('oc')),
                       float(capacity_data.get('mcmn')),
                       float(capacity_data.get('mcmx')),
                       float(capacity_data.get('mc')),
                       float(capacity_data.get('ccsmn')),
                       float(capacity_data.get('ccsmx')),
                       float(capacity_data.get('ccsc')),
                       int(capacity_data.get('ygc')),
                       int(capacity_data.get('fgc'))
                       )]
            cur.executemany(sql,values)

        if gc_data:
            sql = '''insert into jvm_gc(time, app,ip, s0c,s1c,s0u,s1u,ec,eu,oc,ou,mc,mu,ccsc,ccsu,ygct,fgct,ygc,fgc)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            values = [(gc_data.get('time'), gc_data.get('app'), gc_data.get('ip'),
                       float(gc_data.get('s0c')),
                       float(gc_data.get('s1c')),
                       float(gc_data.get('s0u')),
                       float(gc_data.get('s1u')),
                       float(gc_data.get('ec')),
                       float(gc_data.get('eu')),
                       float(gc_data.get('oc')),
                       float(gc_data.get('ou')),
                       float(gc_data.get('mc')),
                       float(gc_data.get('mu')),
                       float(gc_data.get('ccsc')),
                       float(gc_data.get('ccsu')),
                       float(gc_data.get('ygct')),
                       float(gc_data.get('fgct')),
                       int(gc_data.get('ygc')),
                       int(gc_data.get('fgc'))
                       )]
            cur.executemany(sql,values)

        if thread_count_data:
            thread_sql = '''insert into jvm_thread_count(time, app, count, ip)
                    values(%s, %s, %s, %s) ON DUPLICATE KEY
                    UPDATE time=VALUES(time) and app=VALUES(app) and ip=VALUES(ip)'''
            thread_values = [(thread_count_data.get('time'), thread_count_data.get('app'), int(thread_count_data.get('count')), thread_count_data.get('ip'))]
            cur.executemany(thread_sql, thread_values)

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
        collect_gc = app.get('collect_gc')
        collect_capacity = app.get('collect_capacity')
        collect_thread_count = app.get('collect_thread_count')

        j_capacity, j_gc, j_thread = None, None, None
        if collect_capacity:
            j_capacity = collect_jvm_capacity(app, pid)
        if collect_gc:
            j_gc = collect_jvm_gc(app, pid)
        if collect_thread_count:
            j_thread = collect_jvm_thread_count(app, pid)

        push_data_to_mysql(j_gc, j_capacity, j_thread)

