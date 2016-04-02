# -*- coding: utf-8 -*-

import os
import requests
import time
import datetime
import json
from dateutil.relativedelta import relativedelta

from utils import headers
from utils import ww
from utils import rr

dr = 'wdzj'

entries = []
with rr('wdzj', 'entries') as fp:
    for line in fp:
        entries.append((line.strip().split()[0], line.strip().split()[1]))

terms = []
with rr('wdzj', 'terms') as fp:
    for line in fp:
        terms.append((line.strip().split()[0], line.strip().split()[1]))

print('Terms loaded')
print(terms)
print('entries loaded')
print(entries)

url = 'http://shuju.wdzj.com/depth-data.html'
xhr_headers = {
'Host': 'shuju.wdzj.com',
'X-Requested-With': 'XMLHttpRequest',
}

xhr_headers.update(headers)
ref = 'http://shuju.wdzj.com/plat-info-{0}.html'

tdy = datetime.date.today()
now = tdy.strftime("%Y-%m-%d")
past1m = (tdy - relativedelta(months=1)).strftime("%Y-%m")
past1d = (tdy - relativedelta(days=1)).strftime("%Y-%m-%d")
past4m = (tdy - relativedelta(months=4)).strftime("%Y-%m")
past1y = (tdy - relativedelta(years=1)).strftime("%Y-%m-%d")
past1y_monthly = (tdy - relativedelta(years=1)).strftime("%Y-%m")

with ww('wdzj', 'features') as fw:
    fw.write(('Crawled on {0}; Today\'s data exclusive;\n'\
        'Termid and terms:\n' + 
        ''.join(['    {0} {1}\n'.format(x, y) for x, y in terms]) +
        'Timespan:\n'\
        '    For daily in the past year (1-14, 18): {1} ~ {2} inclusive;\n'\
        '    For daily in the future trimonth (15): {3} ~ {4} inclusive;\n'\
        '    For monthly in the past year (16): {5} ~ {6} inclusive;\n'\
        '    For monthly in the past quadmonth (17): {7} ~ {8} inclusive;\n'\
        'Units:\n'\
        '    /万元: 1-4, 7-8, 15\n'\
        '    /月: 10\n'\
        '    /秒: 15 (满标用时)\n'\
        '    /人: 5, 6, 11, 12, 16\n'\
        '    /个: 9\n'\
        ' -*- END OF HEADER -*-\n').format(now, past1y, past1d, '[see below]', '[see below]', past1y_monthly, past1m, past4m, past1m))
    for idx, entrytpl in enumerate(entries):
        entry, name = entrytpl
        xhr_headers['Referer'] = ref.format(entry)
        fw.write('Entries No.{0} PlatId={1} {2}\n'.format(idx + 1, entry, name))
        print('Entries No.{0} PlatId={1} {2}'.format(idx + 1, entry, name))
        for termtpl in terms:
            term, termname = termtpl
            params = {
                'wdzjPlatId': entry,
                'type1': term,
                'type2': '0',
                'status': '0'
            }
            try:
                print url,params
                response = requests.post(url, params=params, headers=xhr_headers, timeout=60)
                z = response.json()
                print(z)
            except KeyboardInterrupt:
                break
            # except:
            #     print('error')
            #     fw.write('[-1] ERROR-IN-CRAWLING-THIS-LINE\n')
            #     continue
            
            if term in {'1', '2', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'}:
                fw.write('{0} {1} {2}\n'.format(term, termname, json.dumps(z.get('y1', 'NO-DATA'))))
            elif term == '3':
                fw.write('{0} {1} {2}\n'.format(term, '当日待还金额', json.dumps(z.get('y1', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '当日待还金额(30日平均)', json.dumps(z.get('y2', 'NO-DATA'))))
            elif term == '15':
                fw.write('{0} {1} {2}\n'.format(term, '未来60日资金流出走势', json.dumps(z.get('y1', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '未来每日还款金额', json.dumps(z.get('y2', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '未来时间段', json.dumps(z.get('x', 'NO-DATA'))))
            elif term == '16':
                fw.write('{0} {1} {2}\n'.format(term, '0-1万投资人', json.dumps(z.get('y1', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '1-10万投资人', json.dumps(z.get('y2', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '10-100万投资人', json.dumps(z.get('y3', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '>100万投资人', json.dumps(z.get('y4', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '1-10万借款人', json.dumps(z.get('y5', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '10-100万借款人', json.dumps(z.get('y6', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '100-1000万借款人', json.dumps(z.get('y7', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '>1000万借款人', json.dumps(z.get('y8', 'NO-DATA'))))
            elif term == '17':
                fw.write('{0} {1} {2}\n'.format(term, '天标 利率', json.dumps(z.get('y1', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '1月标 利率', json.dumps(z.get('y2', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '2月标 利率', json.dumps(z.get('y3', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '3-6月标 利率', json.dumps(z.get('y4', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '>6月标 利率', json.dumps(z.get('y5', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '天标 满标用时', json.dumps(z.get('y6', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '1月标 满标用时', json.dumps(z.get('y7', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '2月标 满标用时', json.dumps(z.get('y8', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '3-6月标 满标用时', json.dumps(z.get('y9', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '>6月标 满标用时', json.dumps(z.get('y10', 'NO-DATA'))))
            elif term == '18':
                fw.write('{0} {1} {2}\n'.format(term, '前十大投资人待收占比', json.dumps(z.get('y1', 'NO-DATA'))))
                fw.write('{0} {1} {2}\n'.format(term, '前五十投资人待收占比', json.dumps(z.get('y2', 'NO-DATA'))))
            else:
                assert(0)
            fw.flush()
            time.sleep(0.01)
        if idx > 3000:
            break










            
