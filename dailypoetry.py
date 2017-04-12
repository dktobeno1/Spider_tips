import re,requests,time,mysql.connector,random,queue
from bs4 import BeautifulSoup

def randHeader():
    user_agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
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

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'User-Agent': random.choice(uer_agents),
               'Connection': 'keep-alive',
               'Host': 'www.zgshige.com'
        }
    return headers

def get_ip():
    list_ip = ['125.88.74.122:81',
               '183.95.80.165:8080',
               '59.37.160.57:8081',
               '124.133.230.254:80',
               '183.78.183.156:82',
               '124.88.67.83:843',
               '42.81.58.199:80',
               '124.88.67.9:80',
               '180.167.34.187:80',
               '183.78.183.156:82',
               '125.88.74.122:85',
               '124.88.67.22:83',
               '14.152.93.79:8080',
               '182.38.36.42:8998',
               '122.96.59.98:82',
               '117.95.19.112:8998',
               '14.127.200.59:8081',
               '221.3.6.2:8081',
               '182.112.128.115:80',
               '124.88.67.9:843',
               '171.8.79.143:8080',
               '180.136.83.16:8998',
               '220.174.236.211:80',
               '124.88.67.17:83',
               '42.81.58.199:80',
               '183.165.150.216:8998',
               '183.78.183.156:82',
               '218.26.227.108:80',
               '124.88.67.9:83',
               '175.30.124.128:80',
               '180.169.59.222:8080',
               '60.250.72.252:8080',
               '222.92.141.250:80',
               '202.107.222.50:80',
               '122.116.229.240:80',
               '112.11.126.198:80',
               '124.88.67.34:82',
               '220.174.236.211:80',
               '119.254.84.90:80',
               '118.122.250.109:80',
               '211.140.151.220:80',
               '118.99.178.21:8080',
               '222.169.193.162:8099',
               '111.207.231.14:8080',
               '112.11.126.202:80',
               '180.167.34.187:80',
               '120.132.6.206:80',
               '122.228.179.178:80',
               '218.4.101.130:83',
               '122.193.14.102:80',
               '111.12.96.188:80',
               '111.7.174.135:80',
               '101.204.163.82:8080',
               '58.52.201.119:8080',
               '183.95.80.165:8080',
               '124.234.157.250:80',
               '112.11.126.197:80',
               '111.206.163.235:80',
               '58.221.38.170:8080',
               '101.230.214.25:8080',
               '220.174.236.211:80',
               '183.78.183.156:82',
               '106.58.127.229:80',
               '112.11.126.202:8080',
               '61.135.217.3:80',
               '111.12.96.188:80',
               '119.254.84.90:80',
               '124.234.157.250:80',
               '112.11.126.204:8080',
               '222.92.141.250:80',
               '106.58.115.12:80',
               '112.11.126.198:8080',
               '60.250.72.252:8080',
               '218.104.148.157:8080',
               '122.229.17.128:80',
               '122.228.179.178:80',
               '202.107.222.50:80',
               '112.11.126.201:8080',
               '42.81.58.199:80',
               '118.99.178.21:8080',
               '14.152.93.79:8080',
               '61.191.41.130:80',
               '42.81.58.198:80',
               '222.73.27.178:80'
        ]
    return list_ip


    
def worker():
    conn = mysql.connector.connect(user = 'root',password = '',database = 'poetry')
    cursor = conn.cursor()
    s = queue.Queue(10)#未爬取成功的诗歌列表页存入s队列
    q = queue.Queue(10)##未爬取成功的诗歌内容页存入q队列
    qishi = 1
    jieshu = 40
    index = qishi - 1#列表页页数
    retry_s = 0#列表页请求重试次数
    proxy_ip = {}
    ip_time = 0
    while True:
        if not s.empty():
            index = s.get()
            retry_s += 1
            if 2 <= retry_s <= 3:
                time.sleep(3)
            elif 4 <= retry_s <= 5:
                time.sleep(6)
            elif 6 <= retry_s <= 7:
                time.sleep(15)
            elif retry_s ==8:
                retry_s = 0
        else:
            index += 1
            retry_s = 0
            if index > jieshu:
                print('>>>>>>>>>>>>>>>>>>>>>> %s -- %s 页诗歌爬取完毕 <<<<<<<<<<<<<<<<<<<<<<'%(qishi,jieshu))
                break
        try:
            if index == 1:
                url_info = 'http://www.zgshige.com/mrhs/index.shtml'
            else:
                url_info = 'http://www.zgshige.com/mrhs/index_%s.shtml'% index
            headers = randHeader()
            if not proxy_ip or (int(time.time()) - ip_time) >= 40:
                proxy_ip = {'http':'http://%s'% random.choice(get_ip())}
                ip_time = int(time.time())
            results_info = requests.get(url_info, headers = headers, proxies = proxy_ip, timeout = 60)
            results_info.encoding = 'utf-8'
            soup = BeautifulSoup(results_info.text, 'lxml')
            list_f = list(soup.select('h4 > a'))
            list_tag = list_f[:-1]
            print('第%s页含有%s首'% (index, len(list_tag)))
            if len(list_tag) == 0:
                proxy_ip = {'http':'http://%s'% random.choice(get_ip())}
                ip_time = int(time.time())
                s.put(index)
                print('%s页爬取失败，压入队列'% index)
                continue
            print('第%s页的诗歌概要爬取成功'% index)
        except:
            proxy_ip = {'http':'http://%s'% random.choice(get_ip())}
            ip_time = int(time.time())
            s.put(index)
            print('%s 页爬取失败，压入队列'% index)
            continue
        #诗歌详情抓取
        i = 0#一页中的第i首诗
        retry_q = 0#诗歌详情爬取重试次数
        while True:
            if not q.empty():
                i = q.get()
                retry_q += 1
                time.sleep(retry_q*1.5)
                if retry_q > 5:
                    
        
        for a in list_tag:
            url = 'http://www.zgshige.com'+a['href']
            result_content = requests.get(url, headers = headers, timeout = 30)
            result_content.encoding = 'utf-8'
            soup_content = BeautifulSoup(result_content.text, 'lxml')
            name = str(soup_content.h3.string)
            span_date = list(soup_content.findAll('span',{'class':'p-l-sm p-r-sm'}))[0]
            date = str(span_date.string)
            author = str(span_date.previous_sibling.string)
            #print(date,author)
            
            list_content = list(soup_content.findAll('section',{'style':re.compile('text-align: .+?; font-size: .+? box-sizing: border-box;')}))
            print(len(list_content))
            if len(list_content) >= 2:
                content = str(list_content[0])
                recommend = str(list_content[1])
                cursor.execute('insert into dailypoetry (name,date,author,content,recommend,url) values (%s,%s,%s,%s,%s,%s)',[name,date,author,content,recommend,url])
            else:
                cursor.execute('insert into dailypoetry (name,date,author,url) values (%s,%s,%s,%s)',[name,date,author,url])
            print('%s导入数据库'% name)
        conn.commit()
    conn.close()

if __name__ == '__main__':
    worker()
