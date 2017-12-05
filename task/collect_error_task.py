# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os
cur_dir = os.path.abspath(__file__)
sys.path.insert(0, '/'.join(cur_dir.split('/')[:-2]))


from collector.error_num_collector import collect_data

if __name__ == '__main__':
    collect_data()

