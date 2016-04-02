
# -*- coding: UTF-8 -*-
import os

import time
import requests
import re
import json

from utils import ww
from utils import headers

dr = 'wdzj'

def getrank():
    p = re.compile(r'target="_blank"><span>(?P<name>.*?)</span></a><a href="javascript:;" class="attention" data-plat="(?P<id>[0-9]*?)"')
    url = 'http://shuju.wangdaizhijia.com/platdata-1.html'
    response = requests.get(url, headers=headers)
    s = response.content.decode('utf-8')

    with ww(dr, 'rank') as fw:
        for x in p.finditer(s):
            fw.write(' '.join([x.group('id'), x.group('name'), '\n']))

def getentry():
    url = 'http://shuju.wangdaizhijia.com/plat-info-{0}.html'
    p_name = re.compile(r'<title>(?P<name>.+?)官网数据档案_网贷之家</title>')
    p_capital = re.compile(r'<li><span>注册资本：</span><span><i>(?P<capital>[0-9]*?)</i>万元</span>')
    p_since = re.compile(r'<li><span>上线时间：</span><span>(?P<since>[0-9\-]*?)</span></li>')
    p_rtrn = re.compile(r'<li><span>平均年化：</span><span><i>(?P<rtrn>[0-9\.]*?)</i>%</span></li>')

    try:
        with ww(dr, 'entries', 'r') as fp:
            last = max([int(x.strip().split()[0]) for x in fp.readlines()])
    except (FileNotFoundError, ValueError):
        last = 1

    with ww(dr, 'entries', 'a') as fw:
        for idx in range(last, 4500):
        #for idx in [1,60]:
            response = requests.get(url.format(idx), headers=headers)
            s = response.content.decode('utf-8')
            j = p_name.search(s)
            print(idx)
            if j:
                capital = p_capital.search(s).group('capital')
                since = p_since.search(s).group('since')
                rtrn = p_rtrn.search(s).group('rtrn')
                fw.write('{0} {1} {2} {3} {4}\n'.format(idx, j.group('name'), capital, since, rtrn))
                fw.flush()
                print(j.group('name'))
            time.sleep(0.4)
#getrank()
getentry()
