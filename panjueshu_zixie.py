import random,queue,multiprocessing,re,json,time,requests,mysql.connector


    
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

def get_ips():  # 获取代理ip地址，tm时间进行更新
    ip_url = 'http://s.zdaye.com/?api=201612191506234219&count=200&fitter=2&px=2'
    header = {'Connection': 'close'}
    while True:
        try:
            obtain = requests.get(ip_url, headers=header, timeout=300)
            if '<bad>' not in obtain.text:
                break
        except:
            time.sleep(3)
            continue
    ip_list = obtain.text.split('\r\n')
    return ip_list    


def fail_handler():
    proxy_ip = []
    ip_time = 0
    conn = mysql.connector.connect(user="root", password="", database="caipan")
    cursor = conn.cursor()
    while 1:
        sql = 'select * from failure where content is Null order by id asc limit 10'
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            for nrows in results:
                doc_url = nrows[3]
                id = nrows[0]
                for i in range(5):
                    try:
                        headers = randHeader()
                        time.sleep(i * 2)
                        time.sleep(random.randint(0, 2) + random.random())
                        while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                            proxy_ip = get_ips()
                            ip_time = int(time.time())
                        proxies = {'http': 'http://' + random.choice(proxy_ip)}
                        html = requests.get(doc_url, proxies=proxies, headers=headers[1], timeout=5)
                        re_content = re.compile('jsonHtmlData = "(.*?)";')
                        content = re.findall(re_content,html.text)[0].replace("\"", "\'")
                        sql = 'update failure set content="%s" where id="%s"' % (content, id)
                        cursor.execute(sql)
                        conn.commit()
                        print ('%s条数据已填充') % id
                        break
                    except Exception:
                        print ("(Get) %s次抓取未成功,压入队列 ") % i
                        print (doc_url)
                        continue

        else:
            print ('>>>>>>>>>>>>> Fail 补充抓取完成 <<<<<<<<<<<<<<')
            sql = 'insert into panjueshu (name, yiju, docid, area, produce, type, num, court, date, content, url) select name, yiju, docid, area, produce, type, num, court, date, content, url from failure'
            cursor.execute(sql)
            conn.commit
            conn.close()
            break



def worker(que):
    qishi = (que.get()-1)*20+1  # 起始页
    print(qishi)
    proxy_ip = []
    ip_time = 0
    s = queue.Queue(10)  # 案件概要请求未成功队列
    q = queue.Queue(10)  # 案件详情请求未成功队列
    conn = mysql.connector.connect(user="root", password="", database="caipan")
    cursor = conn.cursor()
    the_url = 'http://wenshu.court.gov.cn/List/ListContent'
    jieshu = qishi*20  # 结束页
    index = qishi-1  # 当前页数减一
    try_j = 0  # post尝试次数
    #sum, cycle = judge_span(year, province)  # sum 地区总时间案件总数， times 总的次数，
    #span = 0
    #number = cycle - 1  # span要不断增加，number为定值，需分开赋值
    #front, back = get_date(span, number)  # 抓取时data的日期
    #if sum == 0:
        #time.sleep(3)
    while True:
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
            if index > jieshu:
                print ('>>>>>>>>>>>>> %s -- %s 页文书已抓取完成  <<<<<<<<<<<<<<') % (qishi,jieshu)
                break
        try:
            data = {'Param':'裁判年份:2016','Page':'20','Order':'法院层级','Index':str(index),
	'Direction':'asc'}
            print ('第 %s 页') %str(index)
            headers = randHeader()
            while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                proxy_ip = get_ips()
                ip_time = int(time.time())
            proxies = {'http': 'http://' + random.choice(proxy_ip)}
            res = requests.post(the_url, data=data, headers=headers[0], proxies=proxies, timeout=60)
            #res.encoding = 'utf-8'
            results = json.loads(res.text)
            try_j = 0
        except:
            s.put(index)
            proxy_ip = get_ips()
            #ip_time = int(time.time())
            print ("(Post)未访问成功，压入队列  ") 
            continue
        print ('案件页数总计 %s -- %s 页,正在抓取 %s 页 ') % (qishi, jieshu, index)
        i = 0  # post一页20个案例，表示一页中第几个案例
        try_i = 0  # get尝试次数
        while True:
            if not q.empty():
                i = q.get()
                try_i += 1
                time.sleep(try_i * 1.5)
                if try_i > 5:
                    fsql = 'insert into failure (name, cause, area, docid, produce, type, num, court, date, yiju, url, doc_url) value("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (name, anyou, province, docid, produce, type, num, court, date, yiju, url, doc_url)
                    cursor.execute(fsql)
                    conn.commit()
                    print ('!!!!!!!!!!!!!!!!!!! 请求过多,%s页第%s个案件:%s 写入Failure表中 !!!!!!!!!!!!!!!!!!!') % (index, i, name)
                    i += 1
                    try_i = 0
                    q.queue.clear()
                    if i >= len(results):
                        break
            else:
                i += 1
                try_i = 0
            name = results[i]['案件名称']  # 案件名称
            docid = results[i]['文书ID']  # 文书ID
            produce = results[i]['审判程序']  # 审判程序
            type = results[i]['案件类型']  # 案件类型
            num = results[i]['案号']  # 案号
            court = results[i]['法院名称']  # 法院名称
            date = results[i]['裁判日期']  # 裁判日期
            yiju = results[i]['裁判要旨段原文']  # 判决依据
            url = 'http://wenshu.court.gov.cn/content/content?DocID=%s' % docid
            doc_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=%s' % docid
            try:
                headers = randHeader()
                time.sleep(random.randint(0, 2) + random.random())
                while not (int(time.time()) - ip_time) < 60 or not proxy_ip:
                    proxy_ip = get_ips()
                    ip_time = int(time.time())
                proxies = {'http': 'http://' + random.choice(proxy_ip)}
                html = requests.get(doc_url, proxies=proxies, headers=headers[1], timeout=5)
                re_content = re.compile('jsonHtmlData = "(.*?)";')
                content = re.findall(re_content,html.text)[0].replace("\"", "\'")
            except Exception:
                q.put(i)
                print ("(Get) %s未抓取成功,压入队列 ") % name
                print(doc_url)
                continue
            print ('.....第 %s 个案件') % i
            sql = 'insert into panjueshu (name, yiju, docid, area, produce, type, num, court, date, content, url) value("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
                name, yiju, docid, area, produce, type, num, court, date, content, url)
            print('insert into datebase')
            cursor.execute(sql)
            if i == len(results) - 1:
                break
        conn.commit()
    if not que.empty():
        worker(que)
    conn.close()


if __name__  == '__main__':
    que = multiprocessing.Queue()
    for i in range(1,6):
        que.put(i)
    n = []
    for a in range(1,6):
        p = multiprocessing.Process(target = worker ,args = (que,))
        p.start()
        n.append(p)
        time.sleep(3)
    for b in n:
        b.join()
    fail_handler()
        
    
