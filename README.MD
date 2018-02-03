# 介绍
到了新公司，想要监控线上服务器资源使用以及异常情况，考虑过高大上的ELK，grelog，但是公司规模小，计算资源奇缺，连ECS都是一个月续费一次。
虽然穷，但是随时掌握线上服务器健康状况到关重要。
怎么办，只能退而求其次，轻量的监控，就开始有了eyegla

eyegla 可以收集线上nginx日志统计数据，应用error统计，应用jvm运行情况数据，以此来观察线上应用的健康状况。
eyegla 是一个轻量的服务器数据收集脚本，只是收集，展示需要结合grafana使用。
什么？ 你不会grafana

- collector  收集器
- conf   配置
- task   cronta任务
- scripts  工具脚本

contab : 通过crontab 定时任务定时收集数据


# 开始
### 依赖
##### pymysql 
跟据自己的系统选择安装方式
- easy_install mysql-python (mix os)
- pip install mysql-python (mix os)
- apt-get install python-mysqldb (Linux Ubuntu)
- cd/usr/ports/databases/py-MySQLdb && make install clean (FreeBSD)
- yum install MySQL-python (linux Fedora, CentOS)
- pip install mysqlclient (Windows)

##### mysql 
版本随意。
建库建表脚本请参考 conf/table.sql 。
修改 conf/mysq.py 里mysql连接 。

##### 部署脚本
- 将项目copy到线上目录 
- 修改 task 中目录 
- 修改 colletor 中的应用配置信息
- 将contab定时配置复制到 contrab -e 中保存
- 开始收集数据

##### 查看数据
使用grafana配置图表监控



