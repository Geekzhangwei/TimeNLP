#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author   :geekzw
@Contact  :1223242863@qq.com
@File     :TestTime.py
@Time     :2020/3/23 11:47 PM
@Software :Pycharm
@Copyright (c) 2020,All Rights Reserved.
"""

import time
import warnings
from TimeNormalizer import TimeNormalizer
from arrow.factory import ArrowParseWarning
warnings.simplefilter("ignore", ArrowParseWarning)


if __name__ == "__main__":
    tn = TimeNormalizer()
    while True:
        query = input("\nINPUT : ")
        ss = time.time()
        # target为待分析语句, timeBase为基准时间, 默认是当前时间
        # print("OUTPUT: ", tn.parse(target=query, timeBase="2019-02-03"))
        print("OUTPUT: ", tn.parse(target=query))
        print("TIME  : {0}ms!".format(round(1000 * (time.time() - ss), 3)))
