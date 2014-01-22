#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: exp-time.py
Author: huxuan
Email: i(at)huxuan.org
Description: Time Efficiency Experiments
"""

import datetime

from online import get_score

def main():
    """docstring for main"""
    time_min = datetime.timedelta.max
    time_max = datetime.timedelta.min
    time_tot = datetime.timedelta()
    lang = 'pmml'
    count = 0
    with open('data/queries.txt') as fin:
        for line in fin:
            count += 1
            # print line
            dummy, time_delta = get_score(line, lang)
            print time_delta
            time_min = min(time_min, time_delta)
            time_max = max(time_max, time_delta)
            time_tot += time_delta
    print 'Min:', time_min
    print 'Max:', time_max
    print 'Ave:', time_tot / count

if __name__ == '__main__':
    main()
