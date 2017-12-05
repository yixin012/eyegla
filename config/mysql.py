# -*- coding: utf-8 -*-
__author__ = 'egbert'

import MySQLdb

conn= MySQLdb.connect(
    host='rm-wz96yq2p0k7cdes0eo.mysql.rds.aliyuncs.com',
    port = 3306,
    user='root',
    passwd='shihengds7@24',
    db ='eyegla',
)


'''
创建数据库

CREATE DATABASE eyegla DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

CREATE TABLE `err_num` (
  `stime` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` int(11) NOT NULL default '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`stime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='异常数量';




'''

