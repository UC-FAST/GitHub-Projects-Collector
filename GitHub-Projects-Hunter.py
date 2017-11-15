"""
文件：GitHub-Projects-Hunter.py
描述：github项目统计
时间：2017.11.14 19:28
GitHub：https://github.com/UC-FAST/GitHub-Projects-GitHub-Projects-Hunter/
"""

import requests
import time
import matplotlib.pyplot as plt

def get(str):
    url = 'https://api.github.com/search/repositories?q=language:' + str
    response = requests.get(url).json()
    if response['incomplete_results'] == True:
        return -1
    return response['total_count']

def plot(label,py,cpp,c,java):
    length = len(label)
    x = list(range(1,length + 1))
    #print(x)
    data = [py[-1],cpp[-1],c[-1],java[-1]]
    data.sort()
    plt.title("GitHub Hunter")
    plt.xlabel("time")
    plt.ylabel("data")
    plt.ylim((data[0],data[-1]))
    plt.plot(x, py,'r', label='python')  
    plt.plot(x, cpp,'b',label='cpp')
    plt.plot(x, c,'m', label='c')  
    plt.plot(x, java,'y',label='java')
    plt.xticks(x, label, rotation=0)  
    plt.legend(bbox_to_anchor=[0.3, 1])
    plt.grid()
    plt.show()  

class incomplete_error(BaseException):
    def message():
        return "incomplete_results"

stop = 0
times = 0
py = []
cpp = []
c = []
java = []
label = []

while True:
    try:
        py.append(get('python'))
        cpp.append(get('cpp'))
        c.append(get('c'))
        java.append(get('java'))

        if py[-1] == -1 or cpp[-1] == -1 or c[-1] == -1 or java[-1] == -1:
            del py[-1]
            del cpp[-1]
            del c[-1]
            del java[-1]
            raise incomplete_error

        result = {'python':py[-1],'c++':cpp[-1],'c':c[-1],'java':java[-1]}
        #print(py)
        #print(cpp)
        #print(c)
        #print(java)

        now_time = time.localtime(time.time())#现在的时间
        label.append(time.strftime("%H:%M:%S",now_time))
        #print(label[-1])
        print(time.strftime('%Y-%m-%d %H:%M:%S',now_time))
        print(sorted(result.items(),key=lambda item:item[1]))
        stop = 0
        times+=1
        #print(times)
        #print(label)
        if times >= 5:
            if len(label) == 11:#如果收集了11次时间，删除列表第一个元素
               del label[0]
            plot(label,py,cpp,c,java)

    except Exception as e:
        if stop != 300:
            stop+=30
        #print(e.message())
        print("遇到错误:" + str(stop) + "秒后重新连接")
        time.sleep(stop)
        #time.sleep(0)
    else:
        time.sleep(60 * 60)
        #time.sleep(60)