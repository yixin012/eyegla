#!/bin/bash

LOGS_PATH=/shiheng/logs/nginx

YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

## 获取昨天的 yyyy-MM-dd
mv ${LOGS_PATH}/access.log ${LOGS_PATH}/access_${YESTERDAY}.log

## 向 Nginx 主进程发送 USR1 信号。USR1 信号是重新打开日志文件
kill -USR1 $(cat /shiheng/logs/nginx/logs/nginx.pid)


