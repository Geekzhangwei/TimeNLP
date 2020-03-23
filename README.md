## Python3 —— 时间关键词提取以及标准化
[TOC]

## 1. 新增说明

ryanInf版本与ryanlnf版本存在一些小问题，进行了修复，以及个性化地新增了几个功能。

> （1）不能识别下星期下礼拜等和周相关的时间，已解决

> （2）在windows下使用有问题，ryanInf给出的方案不能解决这个问题。解决方案：将其中的regex.txt文件放入python的site-packages下
>
> - 例如：D:\Users\Administrator\Anaconda3\Lib\site-packages\TimeConverter-1.0.0-py3.7.egg\resource\regex.txt

> （3）新增关键词以及索引位置的提取，具体见TimeNormalizer.py

## 2. 说明
Time-NLP的python3版本，由于原作者sunfiyes的是python2版本，无法在python3上使用，故ryanlnf修改部分代码，使其可在Python3上使用，但运行发现存在一些bug，并进行了修复。

- 原项目地址：https://github.com/sunfiyes/Time-NLPY  

- Python3项目地址：https://github.com/ryanInf/Time-NLPY

## 3. 安装方式  
> - cd到当前目录

> - python setup.py install

说明：window下可能出现安装regex错误，可到https://www.lfd.uci.edu/~gohlke/pythonlibs/#regex下载对应版本的regex手动安装

## 4. 使用方法
将中文时间描述转换为三种标准的时间格式的时间字符串：

- 时间点（timestamp，表示某一具体时间时间描述）; 

-  时间量（timedelta，表示时间的增量的时间描述）; 

- 时间区间（timespan，有具体起始和结束时间点的时间区间）。

- 

  

运行代码：

> python TestTime.py



TestTime.py代码与示例：

``` python
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
```
输出：

- 默认当前时间

```
INPUT :  昨天上午和2019年8月
OUTPUT:  [['昨天上午', (0, 4), '2020-03-23 10:00:00'], ['2019年8月', (5, 12), '2019-08-01 00:00:00']]
TIME  : 3.734ms!

INPUT : 看今天的新闻以及后天的疫情
OUTPUT:  [['今天', (1, 3), '2020-03-24 00:00:00'], ['后天', (7, 9), '2020-03-26 00:00:00']]
TIME  : 3.657ms!
```


- 自定义基准时间，如2019-02-03

```
INPUT : 昨天上午和2019年8月
OUTPUT:  [['昨天上午', (0, 4), '2019-02-02 10:00:00'], ['2019年8月', (5, 12), '2019-08-01 00:00:00']]
TIME  : 4.585ms!

INPUT : 看今天的新闻以及后天的疫情
OUTPUT:  [['今天', (1, 3), '2019-02-03 00:00:00'], ['后天', (7, 9), '2019-02-05 00:00:00']]
TIME  : 3.73ms!
```



关于节假日的增加方法：  
1) 在resource目录下的holi_lunar(阴历)或holi_solar(阳历)文件内按照格式加入新增的节日名称和日期
2) 在resource目录下的regex.txt文件内加入相应节日的正则匹配，并删除regex.pkl缓存文件
3) 在TimeUnit类中的norm_setHoliday方法同样加入节日的正则匹配

该功能完善中...