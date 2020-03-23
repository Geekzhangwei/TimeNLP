#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@Author   :geekzw
@Contact  :1223242863@qq.com
@File     :TimeNormalizer.py
@Time     :2020/3/23 11:47 PM
@Software :Pycharm
@Copyright (c) 2020,All Rights Reserved.
"""


import pickle
import regex as re
import arrow
import json
import os

from StringPreHandler import StringPreHandler
from TimePoint import TimePoint
from TimeUnit import TimeUnit


# 时间表达式识别的主要工作类
class TimeNormalizer:
    def __init__(self, isPreferFuture=True):
        self.isPreferFuture = isPreferFuture
        self.pattern, self.holi_solar, self.holi_lunar = self.init()

    def init(self):
        fpath = os.path.dirname(__file__) + '/resource/reg.pkl'
        try:
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        except:
            with open(os.path.dirname(__file__) + '/resource/regex.txt', 'r', encoding='utf-8-sig') as f:
                content = f.read()
            p = re.compile(str(content))
            with open(fpath, 'wb') as f:
                pickle.dump(p, f)
            with open(fpath, 'rb') as f:
                pattern = pickle.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_solar.json', 'r', encoding='utf-8-sig') as f:
            holi_solar = json.load(f)
        with open(os.path.dirname(__file__) + '/resource/holi_lunar.json', 'r', encoding='utf-8-sig') as f:
            holi_lunar = json.load(f)
        return pattern, holi_solar, holi_lunar

    def parse(self, target, timeBase=arrow.now()):
        """
        TimeNormalizer的构造方法，timeBase取默认的系统当前时间
        :param timeBase: 基准时间点
        :param target: 待分析字符串
        :return: 时间单元数组
        """
        self.isTimeSpan = False
        self.invalidSpan = False
        self.timeSpan = ''
        self.target = str(target)
        self.timeBase = arrow.get(timeBase).format('YYYY-M-D-H-m-s')
        self.oldTimeBase = self.timeBase
        self.__preHandling()
        self.timeToken = self.__timeEx()
        dic = []
        res = self.timeToken

        if len(res) == 0:
            return dic
        else:
            for exp_time in res:
                dic.append([exp_time.exp_time, (exp_time.start_index, exp_time.end_index),
                            exp_time.time.format("YYYY-MM-DD HH:mm:ss")])
        return dic

    def __preHandling(self):
        """
        待匹配字符串的清理空白符和语气助词以及大写数字转化的预处理
        :return:
        """
        self.target = StringPreHandler.delKeyword(self.target, "\\s+")   # 清理空白符
        self.target = StringPreHandler.delKeyword(self.target, "[的]+")  # 清理语气助词
        self.target = StringPreHandler.numberTranslator(self.target)     # 大写数字转化

    def __timeEx(self):
        """
        :param target: 输入文本字符串
        :param timeBase: 输入基准时间
        :return: TimeUnit[]时间表达式类型数组
        """
        startline = -1
        endline = -1
        rpointer = 0
        temp = []
        match = self.pattern.finditer(self.target)
        for m in match:
            startline = m.start()
            if startline == endline:
                rpointer -= 1
                index = temp[rpointer][1] + m.span()
                temp[rpointer] = (temp[rpointer][0] + m.group(), (index[0], index[-1]))
            else:
                temp.append((m.group(), m.span()))
            endline = m.end()
            rpointer += 1
        res = []
        # 时间上下文： 前一个识别出来的时间会是下一个时间的上下文，用于处理：周六3点到5点这样的多个时间的识别，第二个5点应识别到是周六的。
        contextTp = TimePoint()
        for i in range(0, rpointer):
            res.append(TimeUnit(temp[i], self, contextTp))
            contextTp = res[i].tp
        res = self.__filterTimeUnit(res)
        return res

    def __filterTimeUnit(self, tu_arr):
        """
        过滤timeUnit中无用的识别词。无用识别词识别出的时间是1970.01.01 00:00:00(fastTime=0)
        :param tu_arr:
        :return:
        """
        if (tu_arr is None) or (len(tu_arr) < 1):
            return tu_arr
        res = []
        for tu in tu_arr:
            if tu.time.timestamp != 0:
                res.append(tu)
        return res
