"""
文件：PythonApplication2.py
描述：github项目统计
时间：2017.11.14 19:28
GitHub：https://github.com/UC-FAST/GitHub-Projects-Collector/
"""

import requests
import time

def get(str):
    url = 'https://api.github.com/search/repositories?q=language:' + str
    response = requests.get(url).json()
    if response['incomplete_results'] == True:
        return -1
    return response['total_count']

stop=0

while True:
    try:
        result = {
            'python':get('python'),
                'c++':get('cpp'),
                'c':get('c'),
                'java':get('java')}
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print(sorted(result.items(),key=lambda item:item[1]))
    except:
        if stop!=300:
            stop+=30
        print("遇到错误，"+str(stop)+"秒后重新连接")
        time.sleep(stop)
    else:
        time.sleep(60*60)


