



CREATE TABLE `jvm_capacity` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `time` datetime NOT NULL COMMENT '时间',
  `app` varchar(20) NOT NULL COMMENT '应用名称',
  `ngcmn` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '新生代min',
  `ngcmx` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '新生代max',
  `ngc` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '新生代容量',
  `s0c` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '第一幸存区大小',
  `s1c` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '第二幸存区大小',
  `ec` decimal(11,1) NOT NULL DEFAULT '0' COMMENT 'eden区大小',
  `ogcmn` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '老年代最小容量',
  `ogcmx` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '老年代最大容量',
  `ogc` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '老年代大小',
  `oc` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '老年代大小',
  `mcmn` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '最大元数据容量',
  `mcmx` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '最小元数据容量',
  `mc` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '当前元数据空间大小',
  `ccsmn` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '最小压缩类空间大小',
  `ccsmx` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '最大压缩类空间大小',
  `ccsc` decimal(11,1) NOT NULL DEFAULT '0' COMMENT '当前类压缩空间大小',
  `ygc` int(4) NOT NULL DEFAULT '0' COMMENT '年轻代gc次数',
  `fgc` int(4) NOT NULL DEFAULT '0' COMMENT 'full gc次数',
  `ip` varchar(20) NOT NULL DEFAULT '127.0.0.1' COMMENT 'ip',
  PRIMARY KEY (`id`),
  KEY `index_time_app` (`time`,`app`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='jvm capacity';



