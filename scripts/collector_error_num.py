# -*- coding: utf-8 -*-
__author__ = 'egbert'

import sys
import os
cur_dir = os.path.abspath(__file__)
sys.path.insert(0, '/'.join(cur_dir.split('/')[:-2]))


from collector.error_num_collector import collect_data_by_date


if __name__ == '__main__':

    collect_data_by_date('2017-12-04 13:39')

    # arger = argparse.ArgumentParser(__file__)
    # arger.add_argument('-min', type=int, help=u'an id a line file')
    # arger.add_argument('-max', type=int, help=u'action of the msg')
    # arger.add_argument('-limit', type=int, help=u'action of the msg')
    # args = arger.parse_args()
    #
    # min = args.min
    # max = args.max
    # limit = args.limit
