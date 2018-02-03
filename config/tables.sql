

CREATE DATABASE eyegla DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;

CREATE TABLE `err_num` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `stime` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`stime`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=188673 DEFAULT CHARSET=utf8 COMMENT='异常数量';

CREATE TABLE `jvm_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `ngcmn` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '新生代min',
  `ngcmx` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '新生代max',
  `ngc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '新生代容量',
  `s0c` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '第一幸存区大小',
  `s1c` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '第二幸存区大小',
  `ec` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'eden区大小',
  `ogcmn` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '老年代最小容量',
  `ogcmx` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '老年代最大容量',
  `ogc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '老年代大小',
  `oc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '老年代大小',
  `mcmn` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '最大元数据容量',
  `mcmx` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '最小元数据容量',
  `mc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '当前元数据空间大小',
  `ccsmn` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '最小压缩类空间大小',
  `ccsmx` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '最大压缩类空间大小',
  `ccsc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '当前类压缩空间大小',
  `ygc` int(4) NOT NULL DEFAULT '0' COMMENT '年轻代gc次数',
  `fgc` int(4) NOT NULL DEFAULT '0' COMMENT 'full gc次数',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=22471 DEFAULT CHARSET=utf8 COMMENT='jvm capacity';

CREATE TABLE `jvm_gc` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `s0c` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'so容量',
  `s1c` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 's1容量',
  `s0u` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'so使用量',
  `s1u` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 's1使用量',
  `ec` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'eden容量',
  `eu` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'eden使用量',
  `oc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'old容量',
  `ou` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'old使用量',
  `mc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'metaspace容量',
  `mu` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT 'metaspace使用量',
  `ccsc` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '类压缩空间容量',
  `ccsu` decimal(11,1) NOT NULL DEFAULT '0.0' COMMENT '类压缩空间使用量',
  `ygct` decimal(11,6) NOT NULL DEFAULT '0.000000' COMMENT 'ygc time',
  `fgct` decimal(11,6) NOT NULL DEFAULT '0.000000' COMMENT 'fgc time',
  `ygc` int(4) NOT NULL DEFAULT '0' COMMENT '年轻代gc次数',
  `fgc` int(4) NOT NULL DEFAULT '0' COMMENT 'full gc次数',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=346337 DEFAULT CHARSET=utf8 COMMENT='jvm gc';

CREATE TABLE `jvm_thread_count` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `count` int(11) NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=313907 DEFAULT CHARSET=utf8 COMMENT='jvm thread count';

CREATE TABLE `nginx_num_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=72218 DEFAULT CHARSET=utf8 COMMENT='nginx访问ip数量(分钟)';

CREATE TABLE `nginx_num_m` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=176367 DEFAULT CHARSET=utf8 COMMENT='nginx数量(分钟)';

CREATE TABLE `nginx_num_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` int(11) NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=165959 DEFAULT CHARSET=utf8 COMMENT='nginx数量(分钟)';

CREATE TABLE `nginx_request_time_avg` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `num` float NOT NULL DEFAULT '0' COMMENT '数值',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB AUTO_INCREMENT=6321 DEFAULT CHARSET=utf8 COMMENT='nginx requestime avg';






