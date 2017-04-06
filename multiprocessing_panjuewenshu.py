# -*- coding: utf-8 -*-
"""********** 裁判文书网抓取多进程版 **********"""
import re
import time
import math
import json
import Queue
import random
import requests
import MySQLdb
import datetime
import multiprocessing
from dateutil.relativedelta import relativedelta

pn = 16      # 程序进程数
year = 2016  # 裁判文书抓去年度
anyou = '房屋买卖合同纠纷'  # 裁判文书案由
table = 'contract_dispute'  # 注意查看数据库是否正确
table_fail = 'fail'


def req_ips(tm):  # 获取代理ip地址，tm时间进行更新
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="password", db="civil", charset="utf8")
    cursor = conn.cursor()
    ip_url = 'http://s.zdaye.com/?api=201612191506234219&count=200&fitter=2&px=2'
    header = {'Connection': 'close'}
    while True:
        while True:
            try:
                obtain = requests.get(ip_url, headers=header, timeout=300)
                if u'<bad>' not in obtain.text.decode('utf-8'):
                    break
            except Exception:
                time.sleep(3)
                continue
            except requests.exceptions.Timeout:
                time.sleep(3)
                continue
        ip_list = obtain.text.split('\n')
        sql = "replace into dynamic_ips (ip) values (%s)"
        cursor.executemany(sql, map(lambda x: (x,), ip_list))
        conn.commit
        time.sleep(tm)
        tsql = "truncate table dynamic_ips"
        cursor.execute(tsql)
        conn.commit
def get_ips():
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="password", db="abnormal_operation", charset="utf8")
    cursor = conn.cursor()
    sql = 'select ip from dynamic_ip'
    cursor.execute(sql)
    results = map(lambda x: list(x), cursor.fetchall())
    conn.close
    return results
def randHeader():  # 随机获取headers头
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    header = [
        {
            'Host': 'wenshu.court.gov.cn',
            'User-Agent': random.choice(head_user_agent),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive'},
        {
            'Host': 'wenshu.court.gov.cn',
            'User-Agent': random.choice(head_user_agent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'}
    ]
    return header
def judge_span(year, province):
    proxy_ip = []
    ip_time = 0
    the_url = 'http://wenshu.court.gov.cn//List/ListContent'
    data1 = {'Param': '案由:%s,裁判日期:%s-01-01 TO %s-12-31,法院地域:%s' % (anyou, year, year, province), 'Index': '1',
             'Page': '5', 'Order': '法院层级', 'Direction': 'asc'}
    for i in range(1, 11):
        try:
            headers = randHeader()
            while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                proxy_ip = get_ips()
                ip_time = int(time.time())
            proxies = {'http': 'http://' + random.choice(proxy_ip)[0].strip()}
            res = requests.post(the_url, data=data1, headers=headers[0], proxies=proxies, timeout=60)
            res.encoding = 'utf-8'
            results = json.loads(json.loads(res.text))
            sum = int(results[0][u'Count'])
            break
        except:
            time.sleep(i * 2)
            print '案由：%s ，%s 年 文书总数抓取失败，重试第 %s 次' % (anyou, year, i)
            continue

    cycle = 0
    if sum != 0:
        times = math.ceil(sum / 750.0)
        cycle = 366 / int(times)
    return sum, cycle
def get_date(span, number):
    startdate = datetime.date(year, 01, 01)
    front = startdate + relativedelta(days=span)
    back = startdate + relativedelta(days=span + number)
    enddate = datetime.date(year, 12, 31)
    if front < enddate and back >= enddate:
        back = enddate
    return front, back
def fail_handle():
    proxy_ip = []
    ip_time = 0
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="password", db="civil", charset="utf8")
    cursor = conn.cursor()
    while 1:
        sql = 'select * from %s where content is Null order by id asc limit 10' % table_fail
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            for nrows in results:
                doc_url = nrows[13]
                id = nrows[0]
                for i in range(5):
                    try:
                        headers = randHeader()
                        time.sleep(i * 2)
                        time.sleep(random.randint(0, 2) + random.random())
                        while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                            proxy_ip = get_ips()
                            ip_time = int(time.time())
                        proxies = {'http': 'http://' + random.choice(proxy_ip)[0].strip()}
                        html = requests.get(doc_url, proxies=proxies, headers=headers[1], timeout=5)
                        re_content = re.compile('jsonHtmlData = "(.*?)";')
                        content = re_content.findall(html.text.encode('utf-8'), re.S)[0].replace("\"", "\'")
                        sql = 'update %s set content="%s" where id="%s"' % (table_fail, content, id)
                        cursor.execute(sql)
                        conn.commit()
                        print '%s条数据已填充' % id
                        break
                    except Exception:
                        print "(Get) %s次抓取未成功,压入队列 " % i
                        print doc_url
                        continue

        else:
            print '>>>>>>>>>>>>> Fail 补充抓取完成 <<<<<<<<<<<<<<'
            sql = 'insert into %s(name, cause, area, docid, produce, type, num, court, date, yiju, content, url) select name, cause, area, docid, produce, type, num, court, date, yiju, content, url from %s' % (
                table, table_fail)
            cursor.execute(sql)
            conn.commit
            conn.close()
            break

def worker(que):
    province = que.get()  # 主进程中省份列表取出省份
    print province
    proxy_ip = []
    ip_time = 0
    s = Queue.Queue(10)  # 案件数目请求未成功队列
    q = Queue.Queue(10)  # 案件详情请求未成功队列
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="password", db="civil", charset="utf8")
    cursor = conn.cursor()
    the_url = 'http://wenshu.court.gov.cn//List/ListContent'
    total = 100  # 总页数设定初值，后面会重新赋值
    index = 0  # 当前页数减一
    try_j = 0  # post尝试次数
    sum, cycle = judge_span(year, province)  # sum 地区总时间案件总数， times 总的次数，
    span = 0
    number = cycle - 1  # span要不断增加，number为定值，需分开赋值
    front, back = get_date(span, number)  # 抓取时data的日期
    if sum == 0:
        time.sleep(3)
    while sum:
        if not s.empty():  # 判断是否有未获取响应的post
            index = s.get()
            try_j += 1
            if 2 <= try_j <= 3:
                time.sleep(3)
            elif 4 <= try_j <= 5:
                time.sleep(6)
            elif try_j == 6:
                time.sleep(10)
            elif try_j == 7:
                time.sleep(120)
            elif try_j > 8:
                try_j = 0
        else:
            index += 1
            if index > total:
                span += cycle
                front, back = get_date(span, number)  # span表示日期跨度，get_date有相关值
                index = 1
                if back > datetime.date(year, 12, 31):
                    print '>>>>>>>>>>>>>anyou：%s，area：%s ,tiem：%s 年 文书已抓取完成  <<<<<<<<<<<<<<' % (anyou, province, front)
                    break
        try:
            data = {'Param': '案由:%s,裁判日期:%s TO %s,法院地域:%s' % (anyou, front, back, province), 'Index': '%s' % index,
                    'Page': '20', 'Order': '法院层级', 'Direction': 'asc'}
            print 'area: %s, time: %s to %s ' % (province, front, back)
            headers = randHeader()
            while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                proxy_ip = get_ips()
                ip_time = int(time.time())
            proxies = {'http': 'http://' + random.choice(proxy_ip)[0].strip()}
            res = requests.post(the_url, data=data, headers=headers[0], proxies=proxies, timeout=60)
            res.encoding = 'utf-8'
            results = json.loads(json.loads(res.text))
            try_j = 0
        except Exception:
            s.put(index)
            print "(Post)未访问成功，压入队列 %s " % data
            continue
        count = int(results[0][u'Count'])  # 选择案件总数
        yu = count / 20
        mo = count % 20
        if yu == 0:  # 计算页数
            total = 1
        elif yu != 0 and mo == 0:
            total = yu
        elif yu != 0 and mo != 0:
            total = yu + 1
        print '案件页数总计 %s 页,正在抓取 %s 页 ' % (total, index)
        i = 0  # post一页20个案例，表示一页中第几个案例
        try_i = 0  # get尝试次数
        while 1:
            if not q.empty():
                i = q.get()
                try_i += 1
                time.sleep(try_i * 1.5)
                if try_i > 5:
                    fsql = 'insert into %s(name, cause, area, docid, produce, type, num, court, date, yiju, url, doc_url) value("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                        table_fail, name, anyou, province, docid, produce, type, num, court, date, yiju, url, doc_url,)
                    cursor.execute(fsql)
                    conn.commit()
                    print '!!!!!!!!!!!!!!!!!!! 请求过多,%s页第%s个案件:%s 写入Fail表中 !!!!!!!!!!!!!!!!!!!' % (index, i, name)
                    i += 1
                    try_i = 0
                    q.queue.clear()
                    if i >= len(results):
                        break
            else:
                i += 1
                try_i = 0
            name = results[i][u'\u6848\u4ef6\u540d\u79f0'].encode('utf-8')  # 案件名称
            docid = results[i][u'\u6587\u4e66ID'].encode('utf-8')  # 文书ID
            produce = results[i][u'\u5ba1\u5224\u7a0b\u5e8f'].encode('utf-8')  # 审判程序
            type = results[i][u'\u6848\u4ef6\u7c7b\u578b'].encode('utf-8')  # 案件类型
            num = results[i][u'\u6848\u53f7'].encode('utf-8')  # 案号
            court = results[i][u'\u6cd5\u9662\u540d\u79f0'].encode('utf-8')  # 法院名称
            date = results[i][u'\u88c1\u5224\u65e5\u671f'].encode('utf-8')  # 裁判日期
            yiju = results[i][u'\u88c1\u5224\u8981\u65e8\u6bb5\u539f\u6587'].encode('utf-8')  # 判决依据
            url = 'http://wenshu.court.gov.cn/content/content?DocID=%s' % docid
            doc_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=%s' % docid
            try:
                headers = randHeader()
                time.sleep(random.randint(0, 2) + random.random())
                while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                    proxy_ip = get_ips()
                    ip_time = int(time.time())
                proxies = {'http': 'http://' + random.choice(proxy_ip)[0].strip()}
                html = requests.get(doc_url, proxies=proxies, headers=headers[1], timeout=5)
                re_content = re.compile('jsonHtmlData = "(.*?)";')
                content = re_content.findall(html.text.encode('utf-8'), re.S)[0].replace("\"", "\'")
            except Exception:
                q.put(i)
                print "(Get) %s未抓取成功,压入队列 " % name
                print doc_url
                continue
            print '.....第 %s 个案件' % i
            sql = 'insert into %s(name, cause, area, docid, produce, type, num, court, date, yiju, content, url) value("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                table, name, anyou, province, docid, produce, type, num, court, date, yiju, content, url)
            print 'insert into datebase'
            cursor.execute(sql)
            if i == len(results) - 1:
                break
        conn.commit()
    if not que.empty():
        worker(que)
    conn.close()

if __name__ == "__main__":
    u = multiprocessing.Queue()  # 法院地域的队列
    listbox = ['北京市', '广东省', '浙江省', '江苏省', '河南省', '四川省', '河北省', '山西省', '山东省', '湖北省', '湖南省', '辽宁省', '吉林省', '福建省', '安徽省',
               '黑龙江省', '上海市', '江西省', '内蒙古自治区', '广西壮族自治区', '海南省', '重庆市', '贵州省', '天津市', '云南省', '西藏自治区', '陕西省', '甘肃省',
               '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '新疆维吾尔自治区高级人民法院生产建设兵团分院']
    # listbox = ['山西省', '河北省', '吉林省', '辽宁省', '江苏省', '四川省', '福建省', '河南省', '湖南省', '陕西省', '甘肃省', '宁夏回族自治区']
    for j in listbox:
        u.put(j)
    n = []
    for k in range(pn):
        print '进程 %s' % (k + 1)
        q = multiprocessing.Process(target=worker, kwargs={'que': u})
        q.start()
        n.append(q)
        time.sleep(3)
    for n in n:
        n.join()
    fail_handle()
