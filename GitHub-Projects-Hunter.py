#!/usr/bin/env python3
"""
文件：GitHub-Projects-Hunter.py
描述：github项目统计
时间：2017.11.14 19:28
GitHub：https://github.com/UC-FAST/GitHub-Projects-GitHub-Projects-Hunter/
"""

import requests
import time
# 如果运行于Linux环境加上以下两行
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get(str):
    """
    获取项目信息
    :param str:编程语言对应的名字
    :return: 如果收集失败返回'error'，如果成功返回收集到的信息
    """
    url = 'https://api.github.com/search/repositories?q=language:' + str
    response = requests.get(url).json()
    if response['incomplete_results'] == True or 'message' in response:
        return 'error'
    return response['total_count']


def plot(label, py, cpp, c):
    """
    绘图
    :param label: 时间轴
    :param py: Python列表
    :param cpp: C++列表
    :param c: C语言列表
    :return:没有返回值
    """
    data_max = [py[-1], cpp[-1], c[-1]]
    data_max.sort()
    data_min = [py[1], cpp[1], c[1]]
    data_min.sort()
    length = len(label)
    x = list(range(1, length + 1))
    # print(x)
    plt.title("GitHub Hunter")
    plt.xlabel("time")
    plt.ylabel("data")
    plt.xticks(x, label, rotation=0)
    l1, = plt.plot(x, py, 'r', label='python')
    l2, = plt.plot(x, cpp, 'b', label='cpp')
    l3, = plt.plot(x, c, 'm', label='c')
    plt.legend(handles=[l1, l2, l3], labels=['python', 'cpp', 'c'], loc='best')  # 图例
    plt.ylim(data_min[0], data_max[-1])  # y轴范围
    plt.grid()
    plt.savefig('result.png', dpi=150)
    plt.clf()
    plt.cla()


class IncompleteError(BaseException):
    """
    自定义错误，当信息收集失败时被raise
    """

    @staticmethod
    def message():
        return "incomplete_results"


stop = 60       #遇到异常暂停
py = []
cpp = []
c = []
label = []
times = 1       #收集次数统计
sleepTime = 60  #收集信息间隔
day = 0

while True:
    try:
        now_time = time.localtime(time.time())
        if day != int(time.strftime('%d', now_time)):  # 更新base
            print('重新计数')
            label = []  # 清空记录的数据
            cpp = [0]
            c = [0]
            py = [0]
            now_time = time.localtime(time.time())
            label.append(time.strftime("%H:%M", now_time))  # 第一组数据的获得时间
            print('base start')
            py_base = get('python')
            cpp_base = get('cpp')
            c_base = get('c')
            print('base end')
            day = int(time.strftime('%d', now_time))
            print('日期被更新为', day)
            time.sleep(sleepTime)
            continue

        now_time = time.localtime(time.time())  # 现在的时间
        label.append(time.strftime("%H:%M", now_time))
        # print(label[-1])
        print(time.strftime('%Y-%m-%d %H:%M', now_time))

        # print('start')
        py.append(get('python') - py_base)
        # print(py)
        cpp.append(get('cpp') - cpp_base)
        # print(cpp)
        c.append(get('c') - c_base)
        # print(c)
        # print('end')

        if py[-1] == 'error' or cpp[-1] == 'error' or c[-1] == 'error':
            del py[-1]
            del cpp[-1]
            del c[-1]
            del label[-1]
            raise IncompleteError

        result = {'python': py[-1], 'c++': cpp[-1], 'c': c[-1]}
        print(py)
        print(cpp)
        print(c)

        stop = 0
        times += 1
        print('times:', times)
        print('label:', label)
        if len(label) >= 5:
            if len(label) == 11:  # 如果收集了11次，删除列表第一个元素
                del label[0]
                del py[0]
                del cpp[0]
                del c[0]
            plot(label, py, cpp, c)

    except Exception as e:
        if stop != 3000:
            stop += 60
        #print(e.message())  # 输出错误信息，(不必要)
        print("遇到错误:" + str(stop) + "秒后重新连接")
        time.sleep(stop)
        # time.sleep(0)
    else:
        time.sleep(sleepTime)
