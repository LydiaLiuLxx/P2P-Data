# -*- coding: utf-8 -*-

import os
import time

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
}

def ww(d, f, m='w'):
    t = time.localtime()
    s = time.strftime('%Y-%m-%d', t)
    return open(os.path.join(d, '{0}_{1}'.format(f, s)), m)
    
    
def rr(d, f):
    l = os.listdir(d)
    s = [x[len(f) + 1:] for x in l if x.startswith(f)]
    t = [time.strptime(x, '%Y-%m-%d') for x in s]
    s = time.strftime('%Y-%m-%d', max(t))
    return open(os.path.join(d, '{0}_{1}'.format(f, s)))
